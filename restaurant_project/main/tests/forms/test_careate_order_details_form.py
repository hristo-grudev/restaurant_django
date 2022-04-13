from django import test as django_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from restaurant_project.main.forms.waiters_forms import CreateOrderDetailsForm
from restaurant_project.main.models import Tables, Categories, FoodAndDrinks, Orders

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

    def test_create_order_details_form_when_valid(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Cooks',
        )
        category = Categories.objects.create(
            name='Test cat',
            group=group,
        )
        food = FoodAndDrinks.objects.create(
            name='Test food',
            category=category,
            price=10,
            user=user
        )

        table = Tables.objects.create(
            name='Test',
            max_seats=4,
        )

        order = Orders.objects.create(
            table=table,
            waiter=user
        )

        data = {
            'order': order,
            'food_and_drinks': food,
            'pcs': 5,

        }
        form = CreateOrderDetailsForm(data)
        self.assertTrue(form.is_valid())


    def test_create_order_form_when_invalid(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Cooks',
        )
        category = Categories.objects.create(
            name='Test cat',
            group=group,
        )
        food = FoodAndDrinks.objects.create(
            name='Test food',
            category=category,
            price=10,
            user=user
        )

        table = Tables.objects.create(
            name='Test',
            max_seats=4,
        )

        order = Orders.objects.create(
            table=table,
            waiter=user
        )

        data = {
            'order': order,
            'food_and_drinks': food,
            'pcs': -5,

        }
        form = CreateOrderDetailsForm(data)
        self.assertFalse(form.is_valid())
