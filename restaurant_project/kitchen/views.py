from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView, TemplateView

from restaurant_project.kitchen.forms import EditItemFrom, DeleteOrderDetailsForm, CompleteItemForm, CreateItemFrom
from restaurant_project.kitchen.models import FoodAndDrinks
from restaurant_project.waiters.models import Orders, OrderDetails


class KitchenHomeView(TemplateView):
    template_name = 'kitchen/kitchen_home.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group_all = self.request.user.groups.all()
        user_group = user_group_all[0]
        order_items = OrderDetails.objects.filter(completed=False).filter(food_and_drinks__category__group=user_group)
        context['order_items'] = order_items
        context['user_group'] = user_group

        return context

    def get_success_url(self):
        return reverse_lazy('kitchen home view')


class ItemEditView(UpdateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_edit.html'
    form_class = EditItemFrom
    success_url = reverse_lazy('kitchen home view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # def get_queryset(self):
    #     return super() \
    #         .get_queryset() \
    #         .prefetch_related('ingredients')


class ItemCreateView(CreateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_create.html'
    form_class = CreateItemFrom
    success_url = reverse_lazy('kitchen home view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    #
    # def get_queryset(self):
    #     return super() \
    #         .get_queryset() \
    #         .prefetch_related('ingredients')


class CompleteItemView(UpdateView):
    model = OrderDetails
    template_name = 'kitchen/complete_item.html'
    form_class = CompleteItemForm

    def get_success_url(self):
        return reverse_lazy('kitchen home view')
