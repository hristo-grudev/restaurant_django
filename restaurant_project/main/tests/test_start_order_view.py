from django import test as django_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from restaurant_project.main.models import Tables, Orders, OrderDetails, FoodAndDrinksToIngredients, FoodAndDrinks, \
    Ingredients, Categories

UserModel = get_user_model()


class TablesViewTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser',
        'password': '12345qew',
    }

    def test_remove_item__expect_to_redirect_to_table_details(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Waiters',
        )
        user.groups.add(group)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        table = Tables.objects.create(
            name='test_table_1',
            max_seats=4,
        )

        order = Orders.objects.create(
            table=table,
            waiter=user,
        )

        category = Categories.objects.create(
            name='testcategory',
            group=group,
            image='image/upload/v1649841043/cjp8t9davigpzdcafvsb.png',
        )

        ingredient1 = Ingredients.objects.create(
            name='вино',
            quantity=10,
            unit='бр',
        )

        drink = FoodAndDrinks.objects.create(
            name='вино',
            category=category,
            price=5,
            user=user,
            image='image/upload/v1649841043/cjp8t9davigpzdcafvsb.png',
        )

        FoodAndDrinksToIngredients.objects.create(
            ingredient=ingredient1,
            food_and_drinks=drink,
            quantity=1,
        )

        OrderDetails.objects.create(
            order=order,
            food_and_drinks=drink,
            pcs=2,
        )

        response = self.client.get(reverse('remove item', kwargs={'pk': 1, 'item_id': 1}))

        expected_url = reverse('table details', kwargs={'pk': table.id})

        self.assertRedirects(response, expected_url)
