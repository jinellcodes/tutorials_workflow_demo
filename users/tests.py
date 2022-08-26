from django.test import TestCase
from django.urls import reverse
import pytest

# Create your tests here.
# We will add a basic integration test to test user login, using a fixture to first create a user to log in
# The django_user_model fixture is a built-in fixture, it acts as a shortcut to accessing the User model for this project
# This fixture creates a new user with the Django create_user method and sets a username and password, then returns both as a tuple
@pytest.fixture
def test_user(db, django_user_model):
    django_user_model.objects.create_user(
        username="test_username", password="test_password")
    return "test_username", "test_password" # This returns a tuple

# Now let's write a function to test that loggin into the app works, using the test_user fixture as a parameter to first add a user
# In this code, the client passed in as a parameter is a built-in "dummy web clitn" provided by Django as part of its testing tools
# Its login method helps us test that we can log into the app, and the test_user fixture makes sure that we have a valid user to test with
def test_login_user(client, test_user):
    test_username, test_password = test_user # This unpacks the tuple
    login_result = client.login(username=test_username, password=test_password)
    assert login_result == True