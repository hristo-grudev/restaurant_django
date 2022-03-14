from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from restaurant_project.accounts.models import RestaurantUser
from restaurant_project.common.helpers import BootstrapFormMixin


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    model = RestaurantUser

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

