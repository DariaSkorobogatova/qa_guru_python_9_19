import requests
from jsonschema import validate
from schema import created_user, success_reg, list_users, single_user


def test_response_structure_get_list_users(base_url):
    response = requests.get(
        url=f'{base_url}/users',
        params={'page': 2}
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=list_users)


def test_response_structure_get_single_user(base_url):
    response = requests.get(
        url=f'{base_url}/users/2'
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=single_user)


def test_response_structure_create_user(base_url):
    job = 'chosen_one'
    name = 'neo'
    response = requests.post(
        url=f'{base_url}/users',
        json={'name': name, 'job': job}
    )
    body = response.json()
    assert response.status_code == 201
    validate(body, schema=created_user)


def test_single_user_not_found(base_url):
    response = requests.get(
        url=f'{base_url}/users/23'
    )
    assert response.status_code == 404
    assert response.json() == {}


def test_resource_ceruleans_pantone_value(base_url):
    response = requests.get(
        url=f'{base_url}/unknown',
        params={'per_page': 1}
    )
    body = response.json()
    assert response.status_code == 200
    assert body.get('data')[0].get('name') == 'cerulean'
    assert body.get('data')[0].get('pantone_value') == '15-4020'


def test_single_resource_not_found(base_url):
    response = requests.get(
        url=f'{base_url}/unknown/23'
    )
    assert response.status_code == 404
    assert response.json() == {}


def test_update_user_name(base_url):
    job = 'cat'
    old_name = 'Black'
    response_create = requests.post(
        url=f'{base_url}/users',
        json={'name': old_name, 'job': job}
    )
    id = response_create.json().get('id')
    job = 'cat'
    new_name = 'White'
    response_update = requests.put(
        url=f'{base_url}/users/{id}',
        json={'name': new_name, 'job': job}
    )
    assert response_update.status_code == 200
    assert response_update.json().get('name') == 'White'


def test_delete_user(base_url):
    job = 'evil'
    name = 'ancient'
    response_create = requests.post(
        url=f'{base_url}/users',
        json={'name': name, 'job': job}
    )
    id = response_create.json().get('id')
    response_delete = requests.delete(
        url=f'{base_url}/users/{id}'
    )
    assert response_delete.status_code == 204


def test_response_structure_successful_register(base_url):
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    response = requests.post(
        url=f'{base_url}/register',
        json={'email': email, 'password': password}
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=success_reg)


def test_token_successful_register(base_url):
    email = 'eve.holt@reqres.in'
    password = 'pistol'
    response = requests.post(
        url=f'{base_url}/register',
        json={'email': email, 'password': password}
    )
    body = response.json()
    assert response.status_code == 200
    assert body.get('token') == 'QpwL5tke4Pnpja7X4'


def test_no_password_failed_register(base_url):
    email = 'test@mail.ru'
    response = requests.post(
        url=f'{base_url}/register',
        json={'email': email}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Missing password'


def test_not_defined_user_failed_register(base_url):
    email = 'kirill1991@outlook.com'
    password = '9ae89e5ca'
    response = requests.post(
        url=f'{base_url}/register',
        json={'email': email, 'password': password}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Note: Only defined users succeed registration'


def test_login(base_url):
    email = 'eve.holt@reqres.in'
    password = 'cityslicka'
    response = requests.post(
        url=f'{base_url}/login',
        json={'email': email, 'password': password}
    )
    assert response.status_code == 200
    assert response.json().get('token') == 'QpwL5tke4Pnpja7X4'


def test_no_password_failed_login(base_url):
    email = 'test@mail.ru'
    response = requests.post(
        url=f'{base_url}/login',
        json={'email': email}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Missing password'

