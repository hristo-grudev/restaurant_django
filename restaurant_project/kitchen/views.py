from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from restaurant_project.kitchen.forms import EditItemFrom, CreateItemFrom
from restaurant_project.kitchen.models import FoodAndDrinks


class KitchenHomeView(ListView):
    template_name = 'kitchen/kitchen_home.html'
    model = FoodAndDrinks


class ItemEditView(UpdateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_edit.html'
    form_class = EditItemFrom
    success_url = reverse_lazy('kitchen home view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super() \
            .get_queryset() \
            .prefetch_related('ingredients')


class ItemCreateView(CreateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_create.html'
    form_class = CreateItemFrom
    success_url = reverse_lazy('kitchen home view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return super() \
            .get_queryset() \
            .prefetch_related('ingredients')
