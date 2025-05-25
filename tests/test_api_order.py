import time
from datetime import datetime
from http import HTTPStatus

from projeto_aplicado.resources.order.enums import OrderStatus
from projeto_aplicado.settings import get_settings

settings = get_settings()
API_PREFIX = settings.API_PREFIX


def test_get_orders(client, orders):
    response = client.get(f'{API_PREFIX}/orders/')
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


def test_get_order_by_id(client, orders):
    response = client.get(f'{API_PREFIX}/orders/{orders[0].id}')
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


def test_get_order_by_id_not_found(client):
    response = client.get(f'{API_PREFIX}/orders/99999999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_create_order(client, itens):
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
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.CREATED
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'created'

    order_response = client.get(f'{API_PREFIX}/orders/{response.json()["id"]}')
    assert order_response.status_code == HTTPStatus.OK

    expected_total = (itens[0].price * 2) + (itens[1].price * 3)
    assert order_response.json()['total'] == expected_total


def test_create_order_single_item(client, itens):
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
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(f'{API_PREFIX}/orders/{response.json()["id"]}')
    assert order_response.status_code == HTTPStatus.OK

    assert order_response.json()['total'] == itens[0].price


def test_update_order(client, orders):
    data = {
        'status': 'COMPLETED',
        'notes': 'Updated order',
    }
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'updated'


def test_update_order_not_found(client):
    data = {
        'status': 'COMPLETED',
        'notes': 'Updated order',
    }
    response = client.patch(f'{API_PREFIX}/orders/99999999', json=data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_delete_order(client, orders):
    response = client.delete(f'{API_PREFIX}/orders/{orders[0].id}')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json()['action'] == 'deleted'


def test_delete_order_not_found(client):
    response = client.delete(f'{API_PREFIX}/orders/1')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json() == {'detail': 'Order not found'}


def test_create_order_with_empty_items(client):
    data = {
        'items': [],
        'notes': 'Empty order',
    }
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_order_with_zero_quantity(client):
    data = {
        'items': [
            {
                'product_id': '1',
                'quantity': 0,
                'price': 10.0,
            }
        ],
    }
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_order_with_negative_price(client):
    data = {
        'items': [
            {
                'product_id': '1',
                'quantity': 1,
                'price': -10.0,
            }
        ],
    }
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_order_created_at_unchanged(client, orders):
    # Get initial created_at
    initial_response = client.get(f'{API_PREFIX}/orders/{orders[0].id}')
    initial_created_at = datetime.fromisoformat(
        initial_response.json()['created_at']
    )

    # Update the order
    data = {
        'status': OrderStatus.COMPLETED,
        'notes': 'Updated order',
    }
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK

    # Verify created_at remains unchanged
    updated_response = client.get(f'{API_PREFIX}/orders/{orders[0].id}')
    updated_created_at = datetime.fromisoformat(
        updated_response.json()['created_at']
    )
    assert updated_created_at == initial_created_at


def test_update_order_updated_at_changes(client, orders):
    # Get initial updated_at
    initial_response = client.get(f'{API_PREFIX}/orders/{orders[0].id}')
    initial_updated_at = datetime.fromisoformat(
        initial_response.json()['updated_at']
    )

    # Wait a moment to ensure timestamp difference
    time.sleep(1)

    # Update the order
    data = {
        'status': OrderStatus.COMPLETED,
        'notes': 'Updated order',
    }
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK

    # Verify updated_at is newer
    updated_response = client.get(f'{API_PREFIX}/orders/{orders[0].id}')
    updated_updated_at = datetime.fromisoformat(
        updated_response.json()['updated_at']
    )
    assert updated_updated_at > initial_updated_at


def test_order_total_with_large_quantity(client, itens):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 999999,
                'price': itens[0].price,
            }
        ],
    }
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(f'{API_PREFIX}/orders/{response.json()["id"]}')
    expected_total = itens[0].price * 999999
    assert order_response.json()['total'] == expected_total


def test_order_total_with_small_price(client, itens):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': 0.01,
            }
        ],
    }
    response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert response.status_code == HTTPStatus.CREATED

    order_response = client.get(f'{API_PREFIX}/orders/{response.json()["id"]}')
    assert order_response.json()['total'] == 0.01  # noqa: PLR2004


def test_order_status_transition_to_pending(client, orders):
    data = {'status': OrderStatus.PENDING}
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_completed(client, orders):
    data = {'status': OrderStatus.COMPLETED}
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_cancelled(client, orders):
    data = {'status': OrderStatus.CANCELLED}
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.OK


def test_order_status_transition_to_invalid_status(client, orders):
    data = {'status': 'INVALID_STATUS'}
    response = client.patch(f'{API_PREFIX}/orders/{orders[0].id}', json=data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_order_locator_not_empty(client, itens):
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
    }
    create_response = client.post(f'{API_PREFIX}/orders/', json=data)
    assert create_response.status_code == HTTPStatus.CREATED

    order_response = client.get(
        f'{API_PREFIX}/orders/{create_response.json()["id"]}'
    )
    locator = order_response.json()['locator']
    assert len(locator) > 0


def test_order_locator_unique(client, itens):
    # Create first order
    data = {
        'items': [
            {
                'product_id': itens[0].id,
                'quantity': 1,
                'price': itens[0].price,
            }
        ],
    }
    create_response1 = client.post(f'{API_PREFIX}/orders/', json=data)
    assert create_response1.status_code == HTTPStatus.CREATED

    # Create second order
    create_response2 = client.post(f'{API_PREFIX}/orders/', json=data)
    assert create_response2.status_code == HTTPStatus.CREATED

    # Get locators
    locator1 = client.get(
        f'{API_PREFIX}/orders/{create_response1.json()["id"]}'
    ).json()['locator']
    locator2 = client.get(
        f'{API_PREFIX}/orders/{create_response2.json()["id"]}'
    ).json()['locator']

    # Verify locators are different
    assert locator1 != locator2
