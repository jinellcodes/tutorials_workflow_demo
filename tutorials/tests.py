from django.test import TestCase
from django.urls import reverse
import pytest
from tutorials.models import Tutorial

# Create your tests here.
# First write a test to make sure that when we reverse the view named home, we get the expected path for the homepage on the website, which is "/"
def test_homepage_access():
    url = reverse('home')
    assert url == "/"

# Next we'll write integration tests to see whether we can successfully interact with the database via Django models/ORM
# This integration test will verify we are able to successfully create a Tutorial object inthe database
# The pytest doesn't have access to the database to run the test unless we add a marker above the test function declaration
# @pytest.mark.django_db
# def test_create_tutorial():
#     tutorial = Tutorial.objects.create(
#         title='Pytest',
#         tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
#         description='Tutorial on how to apply pytest to a Django application',
#         published=True
#     )
#     assert tutorial.title == "Pytest"
# We can convert thie create tutorial function into a fixture so we can write more integration tests that require creating a tutorial object
# This new_tutorial fixture function will create a new tutorial object with the attributes described any time it is used as a parameter in a test function
# Then in that test function, that tutorial object will be available to use under the same name as the function name, new_tutorial
@pytest.fixture
def new_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial

# Add test functions
# These test functions use new_tutorial as a parameter
# This causes the new_tutorial fixture function to be run first when either of these tests are run
# The first test simply checks that the object created by the fixture exists, by searching for an object with the same title
def test_search_tutorials(new_tutorial):
    assert Tutorial.objects.filter(title='Pytest').exists()
# This second test updates the title of the new_tutorial object, saves the udpate, and asserts that a tutorial with the updated name exists in the database
# Inside this test function, new_tutorial refers to the object returned from the fixture function
def test_update_tutorial(new_tutorial):
    new_tutorial.title = 'Pytest-Django'
    new_tutorial.save()
    assert Tutorial.objects.filter(title='Pytest-Django').exists()

# Let's try one more integration test with fixtures to show how multiple fixtures may be used in a test function
# This fixture funcion creates a different Tutorials object
@pytest.fixture
def another_tutorial(db):
    tutorial = Tutorial.objects.create(
        title='More-Pytest',
        tutorial_url='https://pytest-django.readthedocs.io/en/latest/index.html',
        description='Tutorial on how to apply pytest to a Django application',
        published=True
    )
    return tutorial
# Next add a test that uses both fixtures as parameters
# Both the objects returned from the new_tutorial and another_tutorial fixtures are passed in
# The test asserts that the .pk attributes are not equal to the other
def test_compare_tutorials(new_tutorial, another_tutorial):
    assert new_tutorial.pk != another_tutorial.pk