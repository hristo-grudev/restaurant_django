from django import test as django_test
from django.contrib.auth import get_user_model

from restaurant_project.main.forms.waiters_forms import CreateOrderForm
from restaurant_project.main.models import Tables
UserModel = get_user_model()

class CreateOrderFormTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser',
        'password': '12345qew',
    }

    VALID_TABLE_DATA = {
        'name': 'testtable',
        'max_seats': 4,
    }

    def test_create_order_form_when_valid(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        table = Tables.objects.create(**self.VALID_TABLE_DATA)
        data = {
            'table': table,
            'waiter': user,

        }
        form = CreateOrderForm(data)
        self.assertTrue(form.is_valid())


    def test_create_order_form_when_invalid(self):
        table = Tables.objects.create(**self.VALID_TABLE_DATA)
        data = {
            'table': table,
            'waiter': 'testuser',

        }
        form = CreateOrderForm(data)
        self.assertFalse(form.is_valid())
