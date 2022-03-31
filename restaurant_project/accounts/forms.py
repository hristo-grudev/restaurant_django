from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.models import Group

from restaurant_project.accounts.models import Profile
from restaurant_project.common.helpers import BootstrapFormMixin



class CreateProfileForm(BootstrapFormMixin, auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
    )
    picture = forms.URLField()
    description = forms.CharField(
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls('form-control')

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            description=self.cleaned_data['description'],
            gender=self.cleaned_data['gender'],
            user=user,
        )
        customer = Group.objects.get(name='Customers')
        user.groups.add(customer)

        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'description')
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name',
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL',
                }
            ),
        }