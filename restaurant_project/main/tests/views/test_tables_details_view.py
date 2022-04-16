from django import test as django_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from restaurant_project.main.models import Tables, Orders, FoodAndDrinks, Categories, Ingredients, \
    FoodAndDrinksToIngredients, OrderDetails

UserModel = get_user_model()


class TablesViewTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser',
        'password': '12345qew',
    }


    def test_get_correct_group__expect_correct_template(self):
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

        Orders.objects.create(
            table=table,
            waiter=user,
        )



        response = self.client.get(reverse('table details', kwargs={'pk': table.id}))
        self.assertTemplateUsed(response, 'waiters/table_details.html')

    def test_get_dif_group__expect_redirect(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Cooks',
        )
        user.groups.add(group)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        table = Tables.objects.create(
            name='test_table_1',
            max_seats=4,
        )

        Orders.objects.create(
            table=table,
            waiter=user,
        )

        response = self.client.get(reverse('table details', kwargs={'pk': table.id}))
        self.assertEqual(302, response.status_code)

    def test_get_correct_searched_string(self):
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

        Orders.objects.create(
            table=table,
            waiter=user,
        )

        category = Categories.objects.create(
            name='Test cat',
            group=group,
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
        )

        drink_ingredient = FoodAndDrinksToIngredients.objects.create(
            ingredient=ingredient1,
            food_and_drinks=drink,
            quantity=1,
        )
        ''
        response = self.client.get(reverse('table details', kwargs={'pk': table.id})+'?item=вино')

        print(response)

        self.assertEqual([drink], list(response.context['searched_items']))

    def test_get_correct_searched_category(self):
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

        Orders.objects.create(
            table=table,
            waiter=user,
        )

        category = Categories.objects.create(
            name='testcategory',
            group=group,
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
        )

        FoodAndDrinksToIngredients.objects.create(
            ingredient=ingredient1,
            food_and_drinks=drink,
            quantity=1,
        )
        ''
        response = self.client.get(reverse('table details', kwargs={'pk': table.id})+f'?category={category.id}')

        self.assertEqual([drink], list(response.context['items']))

    def test_get_correct_context_data(self):
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
            completed=True,
        )


        response = self.client.get(reverse('table details', kwargs={'pk': table.id}))

        self.assertEqual(user, response.context[0]['user'])
        self.assertEqual(order, response.context[0]['order'])
        self.assertEqual(10, response.context[0]['total_sum'])
        self.assertEqual(1, len(response.context[0]['sent_items']))
