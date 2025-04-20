import pytest
from uuid import uuid4
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from account.models import UserModel
from core.cache import user_registration_cache, magic_link_cache


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "username": "jefferson",
        "email": "jeff@example.com",
        "password": "strongpassword123"
    }


@pytest.mark.django_db
def test_register_view(api_client, user_data):
    response = api_client.post(reverse('register'), data=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'Email de verificação' in response.data['message']
    assert len(user_registration_cache) == 1


@pytest.mark.django_db
def test_verify_registration_view(api_client, user_data):
    token = str(uuid4())
    user_registration_cache[token] = user_data
    url = reverse('verify-registration', args=[token])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data and 'refresh' in response.data
    assert UserModel.objects.filter(email=user_data['email']).exists()
    assert token not in user_registration_cache


@pytest.mark.django_db
def test_verify_registration_invalid_token(api_client):
    url = reverse('verify-registration', args=[uuid4()])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_email_login_success(api_client, user_data):
    user = UserModel.objects.create_user(**user_data)
    response = api_client.post(reverse('email-login'), data={
        'email': user.email,
        'password': user_data['password']
    })

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data and 'refresh' in response.data


@pytest.mark.django_db
def test_email_login_invalid_password(api_client, user_data):
    UserModel.objects.create_user(**user_data)
    response = api_client.post(reverse('email-login'), data={
        'email': user_data['email'],
        'password': 'wrongpass'
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_send_magic_link(api_client, user_data):
    user = UserModel.objects.create_user(**user_data)
    response = api_client.post(reverse('send-magic-link'), data={'email': user.email})

    assert response.status_code == status.HTTP_200_OK
    assert 'Link de login' in response.data['message']
    assert len(magic_link_cache) == 1


@pytest.mark.django_db
def test_magic_link_login_success(api_client, user_data):
    user = UserModel.objects.create_user(**user_data)
    token = str(uuid4())
    magic_link_cache[token] = user.pk
    response = api_client.get(reverse('magic-login', args=[token]))

    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data and 'refresh' in response.data
    assert token not in magic_link_cache


@pytest.mark.django_db
def test_magic_link_login_invalid_token(api_client):
    response = api_client.get(reverse('magic-login', args=[uuid4()]))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
