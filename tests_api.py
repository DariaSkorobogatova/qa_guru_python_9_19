import requests
from jsonschema import validate
from schemas.get_list_users import list_users
from schemas.get_single_user import single_user
from schemas.create_user import created_user
from schemas.successful_register import success_reg


def test_schema_get_list_users():
    response = requests.get(
        url="https://reqres.in/api/users",
        params={"page": 2}
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=list_users)


def test_schema_get_single_user():
    response = requests.get(
        url="https://reqres.in/api/users/2"
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=single_user)


def test_schema_create_user():
    job = "chosen_one"
    name = "neo"
    response = requests.post(
        url="https://reqres.in/api/users",
        json={"name": name, "job": job}
    )
    body = response.json()
    assert response.status_code == 201
    validate(body, schema=created_user)


def test_single_user_not_found():
    response = requests.get(
        url="https://reqres.in/api/users/23"
    )
    assert response.status_code == 404
    assert response.json() == {}


def test_assert_resource_ceruleans_pantone_value():
    response = requests.get(
        url="https://reqres.in/api/unknown",
        params={"per_page": 1}
    )
    body = response.json()
    assert response.status_code == 200
    assert body.get('data')[0].get('name') == 'cerulean'
    assert body.get('data')[0].get('pantone_value') == '15-4020'


def test_single_resource_not_found():
    response = requests.get(
        url="https://reqres.in/api/unknown/23"
    )
    assert response.status_code == 404
    assert response.json() == {}


def test_update_user_name():
    job = "cat"
    old_name = "Black"
    response_create = requests.post(
        url="https://reqres.in/api/users",
        json={"name": old_name, "job": job}
    )
    id = response_create.json().get('id')
    job = "cat"
    new_name = "White"
    response_update = requests.put(
        url=f"https://reqres.in/api/users/{id}",
        json={"name": new_name, "job": job}
    )
    assert response_update.status_code == 200
    assert response_update.json().get('name') == 'White'


def test_delete_user():
    job = "evil"
    name = "ancient"
    response_create = requests.post(
        url="https://reqres.in/api/users",
        json={"name": name, "job": job}
    )
    id = response_create.json().get('id')
    response_delete = requests.delete(
        url=f"https://reqres.in/api/users/{id}"
    )
    assert response_delete.status_code == 204


def test_schema_successful_register():
    email = "eve.holt@reqres.in"
    password = "pistol"
    response = requests.post(
        url="https://reqres.in/api/register",
        json={"email": email, "password": password}
    )
    body = response.json()
    assert response.status_code == 200
    validate(body, schema=success_reg)


def test_token_successful_register():
    email = "eve.holt@reqres.in"
    password = "pistol"
    response = requests.post(
        url="https://reqres.in/api/register",
        json={"email": email, "password": password}
    )
    body = response.json()
    assert response.status_code == 200
    assert body.get('token') == "QpwL5tke4Pnpja7X4"


def test_no_password_failed_register():
    email = "test@mail.ru"
    response = requests.post(
        url="https://reqres.in/api/register",
        json={"email": email}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Missing password'


def test_not_defined_user_failed_register():
    email = "kirill1991@outlook.com"
    password = "9ae89e5ca"
    response = requests.post(
        url="https://reqres.in/api/register",
        json={"email": email, "password": password}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Note: Only defined users succeed registration'


def test_login():
    email = "eve.holt@reqres.in"
    password = "cityslicka"
    response = requests.post(
        url="https://reqres.in/api/login",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200
    assert response.json().get('token') == "QpwL5tke4Pnpja7X4"


def test_no_password_failed_login():
    email = "test@mail.ru"
    response = requests.post(
        url="https://reqres.in/api/login",
        json={"email": email}
    )
    body = response.json()
    assert response.status_code == 400
    assert body.get('error') == 'Missing password'

