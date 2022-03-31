from django.forms import ModelForm, HiddenInput

from restaurant_project.common.helpers import BootstrapFormMixin
from restaurant_project.kitchen.models import FoodAndDrinks, FoodAndDrinksToIngredients
from restaurant_project.waiters.models import OrderDetails, Orders


class EditItemFrom(BootstrapFormMixin, ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls('form-control')

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        item = super().save(commit=False)

        item.user = self.user
        if commit:
            item.save()

        return item

    class Meta:
        model = FoodAndDrinks
        exclude = ('user', 'ingredients',)


class CreateItemFrom(BootstrapFormMixin, ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        item = super().save(commit=False)

        item.user = self.user
        if commit:
            item.save()

        return item

    class Meta:
        model = FoodAndDrinks
        exclude = ('user', 'ingredients',)


class CreateOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Orders
        fields = '__all__'
        widgets = {
            'waiter': HiddenInput(),
            'order_end_date': HiddenInput(),
            'status': HiddenInput(),
            'table': HiddenInput(),

        }


class CreateOrderDetailsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = OrderDetails
        fields = '__all__'
        widgets = {
            'order': HiddenInput(),

        }


class AddIngredientForm(BootstrapFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls('w-25')

    class Meta:
        model = FoodAndDrinksToIngredients
        fields = '__all__'

    def save(self, commit=True):
        # commit false does not persist to database
        # just returns the object to be created
        item = super().save(commit=False)

        food_and_drinks = FoodAndDrinks.objects.filter(id=self.pk)

        item.food_and_drinks = food_and_drinks
        if commit:
            item.save()

        return item
