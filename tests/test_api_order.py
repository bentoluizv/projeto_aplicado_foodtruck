from http import HTTPStatus

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
