from datetime import datetime
from http import HTTPStatus

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_orders(client, orders, admin_headers):
    response = client.get(f'{API_PREFIX}/orders/', headers=admin_headers)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert len(response.json()['orders']) == len(orders)
    assert response.json()['orders'] == [
        {
            'id': order.id,
            'status': order.status,
            'total': order.total,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
            'locator': order.locator,
            'notes': order.notes,
        }
        for order in orders
    ]
    assert response.json()['pagination'] == {
        'offset': 0,
        'limit': 100,
        'total_count': len(orders),
        'page': 1,
        'total_pages': 1,
    }


def test_get_order_by_id(client, orders, admin_headers):
    response = client.get(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=admin_headers
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {
        'id': orders[0].id,
        'status': orders[0].status,
        'total': orders[0].total,
        'created_at': orders[0].created_at.isoformat(),
        'updated_at': orders[0].updated_at.isoformat(),
        'locator': orders[0].locator,
        'notes': orders[0].notes,
    }


def test_get_order_by_id_not_found(client, admin_headers):
    response = client.get(
        f'{API_PREFIX}/orders/99999999', headers=admin_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_create_order(client, itens, attendant_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 2,
                'price': itens[0].price,
            },
            {
                'product_id': itens[1].id,
                'quantity': 3,
                'price': itens[1].price,
            },
        ],
        'notes': 'Test order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'created'

    order_response = client.get(
        f'{API_PREFIX}/orders/{response.json()["id"]}',
        headers=attendant_headers,
    )
    assert order_response.status_code == HTTPStatus.OK

    expected_total = (itens[0].price * 2) + (itens[1].price * 3)
    assert order_response.json()['total'] == expected_total


def test_create_order_single_item(client, itens, attendant_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
        'notes': 'Test order with single item',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(
        f'{API_PREFIX}/orders/{response.json()["id"]}',
        headers=attendant_headers,
    )
    assert order_response.status_code == HTTPStatus.OK

    assert order_response.json()['total'] == itens[0].price


def test_update_order(client, orders, attendant_headers):
    data = {
        'status': 'COMPLETED',
        'notes': 'Updated order',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'updated'


def test_update_order_not_found(client, attendant_headers):
    data = {
        'status': 'COMPLETED',
        'notes': 'Updated order',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/99999999', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_delete_order(client, orders, attendant_headers):
    response = client.delete(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'deleted'


def test_delete_order_not_found(client, attendant_headers):
    response = client.delete(
        f'{API_PREFIX}/orders/1', headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_create_order_with_empty_items(client, attendant_headers):
    data = {
        'items': [],
        'notes': 'Empty order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_order_with_zero_quantity(client, attendant_headers):
    data = {
        'items': [
            {
                'product_id': '1',
                'quantity': 0,
                'price': 10.0,
            }
        ],
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_order_with_negative_price(client, attendant_headers):
    data = {
        'items': [
            {
                'product_id': '1',
                'quantity': 1,
                'price': -10.0,
            }
        ],
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_order_created_at_unchanged(client, orders, attendant_headers):
    # Get initial created_at
    initial_response = client.get(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=attendant_headers
    )
    initial_created_at = datetime.fromisoformat(
        initial_response.json()['created_at']
    )

    # Update the order
    data = {
        'status': OrderStatus.COMPLETED,
        'notes': 'Updated order',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK

    # Verify created_at remains unchanged
    updated_response = client.get(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=attendant_headers
    )
    updated_created_at = datetime.fromisoformat(
        updated_response.json()['created_at']
    )
    assert updated_created_at == initial_created_at


def test_update_order_updated_at_changes(client, orders, attendant_headers):
    # Get initial updated_at
    initial_response = client.get(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=attendant_headers
    )
    initial_updated_at = datetime.fromisoformat(
        initial_response.json()['updated_at']
    )

    # Update the order
    data = {
        'status': OrderStatus.COMPLETED,
        'notes': 'Updated order',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK

    # Verify updated_at changes
    updated_response = client.get(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=attendant_headers
    )
    updated_updated_at = datetime.fromisoformat(
        updated_response.json()['updated_at']
    )
    assert updated_updated_at > initial_updated_at


def test_order_total_with_large_quantity(client, itens, attendant_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1000,
                'price': itens[0].price,
            }
        ],
        'notes': 'Large quantity order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(
        f'{API_PREFIX}/orders/{response.json()["id"]}',
        headers=attendant_headers,
    )
    assert order_response.status_code == HTTPStatus.OK

    expected_total = itens[0].price * 1000
    assert order_response.json()['total'] == expected_total


def test_order_total_with_small_price(client, itens, attendant_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': 0.01,
            }
        ],
        'notes': 'Small price order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(
        f'{API_PREFIX}/orders/{response.json()["id"]}',
        headers=attendant_headers,
    )
    assert order_response.status_code == HTTPStatus.OK

    expected_total = 0.01
    assert order_response.json()['total'] == expected_total


def test_order_status_transition_to_pending(client, orders, attendant_headers):
    data = {
        'status': OrderStatus.PENDING,
        'notes': 'Transition to pending',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_completed(
    client, orders, attendant_headers
):
    data = {
        'status': OrderStatus.COMPLETED,
        'notes': 'Transition to completed',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_cancelled(
    client, orders, attendant_headers
):
    data = {
        'status': OrderStatus.CANCELLED,
        'notes': 'Transition to cancelled',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_invalid_status(
    client, orders, attendant_headers
):
    data = {
        'status': 'INVALID_STATUS',
        'notes': 'Invalid status transition',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_order_locator_not_empty(client, itens, attendant_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
        'notes': 'Order with locator',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(
        f'{API_PREFIX}/orders/{response.json()["id"]}',
        headers=attendant_headers,
    )
    assert order_response.status_code == HTTPStatus.OK
    assert order_response.json()['locator'] is not None


def test_order_locator_unique(client, itens, attendant_headers):
    # Create first order
    data1 = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
        'notes': 'First order',
    }
    response1 = client.post(
        f'{API_PREFIX}/orders/', json=data1, headers=attendant_headers
    )
    assert response1.status_code == HTTPStatus.CREATED

    # Create second order
    data2 = {
        'items': [
            {
                'product_id': itens[1].id,
                'quantity': 1,
                'price': itens[1].price,
            }
        ],
        'notes': 'Second order',
    }
    response2 = client.post(
        f'{API_PREFIX}/orders/', json=data2, headers=attendant_headers
    )
    assert response2.status_code == HTTPStatus.CREATED

    # Verify locators are unique
    order1_response = client.get(
        f'{API_PREFIX}/orders/{response1.json()["id"]}',
        headers=attendant_headers,
    )
    order2_response = client.get(
        f'{API_PREFIX}/orders/{response2.json()["id"]}',
        headers=attendant_headers,
    )
    assert (
        order1_response.json()['locator'] != order2_response.json()['locator']
    )


def test_get_orders_unauthorized(client, orders):
    response = client.get(f'{API_PREFIX}/orders/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_orders_invalid_token(client, orders):
    response = client.get(
        f'{API_PREFIX}/orders/',
        headers={'Authorization': 'Bearer invalid_token'},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_kitchen_cannot_create_order(client, itens, kitchen_headers):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
        'notes': 'Test order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=kitchen_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_kitchen_cannot_update_order(client, orders, kitchen_headers):
    data = {
        'status': 'COMPLETED',
        'notes': 'Updated order',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=kitchen_headers,
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_kitchen_cannot_delete_order(client, orders, kitchen_headers):
    response = client.delete(
        f'{API_PREFIX}/orders/{orders[0].id}', headers=kitchen_headers
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_create_order_with_invalid_product_id(client, attendant_headers):
    data = {
        'items': [
            {
                'product_id': 'invalid_id',
                'quantity': 1,
                'price': 10.0,
            }
        ],
        'notes': 'Test order',
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_order_with_missing_required_fields(client, attendant_headers):
    data = {
        'items': [
            {
                'product_id': '1',
                'quantity': 1,
            }
        ],
    }
    response = client.post(
        f'{API_PREFIX}/orders/', json=data, headers=attendant_headers
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_order_with_invalid_status(client, orders, attendant_headers):
    data = {
        'status': 'INVALID_STATUS',
        'notes': 'Invalid status',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_order_with_invalid_data_type(
    client, orders, attendant_headers
):
    data = {
        'status': 123,  # Should be string
        'notes': 'Invalid data type',
    }
    response = client.patch(
        f'{API_PREFIX}/orders/{orders[0].id}',
        json=data,
        headers=attendant_headers,
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
