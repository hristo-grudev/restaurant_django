from django.core.validators import MinValueValidator
from django.forms import ModelForm, HiddenInput

from restaurant_project.common.helpers import BootstrapFormMixin
from restaurant_project.kitchen.models import FoodAndDrinks, FoodAndDrinksToIngredients
from restaurant_project.waiters.models import OrderDetails, Orders


class EditItemFrom(BootstrapFormMixin, ModelForm):
    NAME_LABEL = "Име на рецепта"
    DESCRIPTION_LABEL = "Описание"
    CATEGORY_LABEL = "Категория"
    PRICE_LABEL = "Цена"
    IMAGE_LABEL = "Текуща снимка"
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls('form-control')
        self.fields['name'].label = self.NAME_LABEL
        self.fields['description'].label = self.DESCRIPTION_LABEL
        self.fields['category'].label = self.CATEGORY_LABEL
        self.fields['price'].label = self.PRICE_LABEL
        self.fields['image'].label = self.IMAGE_LABEL

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
    NAME_LABEL = "Име на рецепта"
    DESCRIPTION_LABEL = "Описание"
    CATEGORY_LABEL = "Категория"
    PRICE_LABEL = "Цена"
    IMAGE_LABEL = "Текуща снимка"
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls('form-control')
        self.fields['name'].label = self.NAME_LABEL
        self.fields['description'].label = self.DESCRIPTION_LABEL
        self.fields['category'].label = self.CATEGORY_LABEL
        self.fields['price'].label = self.PRICE_LABEL
        self.fields['image'].label = self.IMAGE_LABEL

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

    def clean_quantity(self):
        MinValueValidator(FoodAndDrinksToIngredients.QUANTITY_MIN_VALUE)(self.cleaned_data['quantity'])
        return self.cleaned_data['quantity']

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

    def clean_quantity(self):
        MinValueValidator(FoodAndDrinksToIngredients.QUANTITY_MIN_VALUE)(self.cleaned_data['quantity'])
        return self.cleaned_data['quantity']

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
