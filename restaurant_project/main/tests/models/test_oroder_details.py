from django import test as django_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from restaurant_project.main.models import Tables, FoodAndDrinks, Categories, Orders, OrderDetails

UserModel = get_user_model()


class OrderDetailsTest(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser',
        'password': '12345qew',
    }

    def test_order_total_price(self):
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

        order_details = OrderDetails.objects.create(
            order=order,
            food_and_drinks=food,
            pcs=4,

        )

        self.assertEqual(40, order_details.total_price())
