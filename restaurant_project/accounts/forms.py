from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.models import Group

from restaurant_project.accounts.models import RestaurantUser
from restaurant_project.common.helpers import BootstrapFormMixin


class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    model = RestaurantUser

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save()
        customer = Group.objects.get(name='Customers')
        user.groups.add(customer)
        if commit:
            user.save()

        return user
