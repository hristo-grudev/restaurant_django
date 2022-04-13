from django import test as django_test
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from restaurant_project.main.models import Tables, Orders

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

        response = self.client.get(reverse('tables list'))
        self.assertTemplateUsed(response, 'waiters/tables_page.html')

    def test_get_dif_group__expect_redirect(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Cooks',
        )
        user.groups.add(group)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.client.get(reverse('tables list'))
        self.assertEqual(302, response.status_code)

    def test_get_correct_context_data(self):
        user = UserModel.objects.create_user(**self.VALID_USER_CREDENTIALS)
        group = Group.objects.create(
            name='Waiters',
        )
        user.groups.add(group)
        self.client.login(**self.VALID_USER_CREDENTIALS)

        table1 = Tables.objects.create(
            name='test_table_1',
            max_seats=4,
        )

        table2 = Tables.objects.create(
            name='test_table_2',
            max_seats=2,
        )

        Orders.objects.create(
            table=table2,
            waiter=user,
        )


        response = self.client.get(reverse('tables list'))

        self.assertEqual([table1, table2], list(response.context['tables']))
        self.assertEqual([2], response.context['occupied_table'])
