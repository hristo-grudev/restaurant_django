from django import test as django_test
from django.contrib.auth import get_user_model

from restaurant_project.main.models import Tables
UserModel = get_user_model()

class TablesTest(django_test.TestCase):

    def test_table_name(self):
        table = Tables.objects.create(
            name='Test',
            max_seats=4,
        )

        self.assertEqual('Маса: Test', str(table))


