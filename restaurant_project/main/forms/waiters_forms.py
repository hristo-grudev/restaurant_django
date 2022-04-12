from django.forms import ModelForm, HiddenInput

from restaurant_project.main.models import Orders, OrderDetails


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
    class Meta:
        model = OrderDetails
        fields = '__all__'
        widgets = {
            'order': HiddenInput(),

        }
