from django import test as django_test
from django.contrib.auth import get_user_model
from django.urls import reverse

from restaurant_project.accounts.models import Profile

UserModel = get_user_model()


class ProfileDetailsViewTests(django_test.TestCase):
    VALID_USER_CREDENTIALS = {
        'email': 'testuser',
        'password': '12345qew',
    }

    VALID_PROFILE_DATA = {
        'first_name': 'Test',
        'last_name': 'User',
        'picture': 'http://test.picture/url.png',
    }

    def __create_user(self, **credentials):
        return UserModel.objects.create_user(**credentials)

    def __create_valid_user_and_profile(self):
        user = self.__create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(
            **self.VALID_PROFILE_DATA,
            user=user,
        )

        return (user, profile)

    def __get_response_for_profile(self, profile):
        return self.client.get(reverse('details profile', kwargs={'pk': profile.pk}))

    def test_when_opening_not_existing_profile__expect_404(self):
        response = self.client.get(reverse('details profile', kwargs={
            'pk': 1,
        }))

        self.assertEqual(404, response.status_code)

    def test_correct_template(self):
        _, profile = self.__create_valid_user_and_profile()
        self.__get_response_for_profile(profile)
        self.assertTemplateUsed('accounts/profile_details.html')


    def test_when_user_is_owner__expect_is_owner_to_be_true(self):
        _, profile = self.__create_valid_user_and_profile()
        self.client.login(**self.VALID_USER_CREDENTIALS)

        response = self.__get_response_for_profile(profile)

        is_owner = response.context['object'].user.id == profile.user.id

        self.assertTrue(is_owner)

    def test_when_user__is_not_owner__expect_is_owner_to_be_false(self):
        _, profile = self.__create_valid_user_and_profile()

        credentials = {
            'email': 'testuser2',
            'password': '12345qwe',
        }

        new_user = self.__create_user(**credentials)
        self.client.login(**credentials)


        response = self.__get_response_for_profile(profile)

        is_owner = response.context['object'].user.id == new_user.id

        self.assertFalse(is_owner)