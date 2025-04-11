from http import HTTPStatus


def test_home_page_get(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_home_menu_page(client):
    response = client.get('/menu')
    assert response.status_code == HTTPStatus.OK
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'
