from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView

from restaurant_project.kitchen.models import Categories
from restaurant_project.waiters.models import Tables, Orders


class TablesView(ListView):
    template_name = 'waiters/tables_page.html'
    model = Tables
    context_object_name = 'tables'


class TableDetailsView(TemplateView):
    template_name = 'waiters/table_details.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.id})

