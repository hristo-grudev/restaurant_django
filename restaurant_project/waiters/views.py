from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from restaurant_project.common.helpers import group_required
from restaurant_project.common.view_mixins import WaitersAccess
from restaurant_project.kitchen.forms import CreateOrderForm, CreateOrderDetailsForm
from restaurant_project.kitchen.models import Categories, FoodAndDrinks
from restaurant_project.waiters.models import Tables, Orders, OrderDetails


class TablesView(WaitersAccess, ListView):
    template_name = 'waiters/tables_page.html'
    model = Tables

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        orders_data = Orders.objects.filter(status=False)
        context['tables'] = Tables.objects.all()
        context['occupied_table'] = [order.table_id for order in orders_data]

        return context


class TableDetailsView(WaitersAccess, TemplateView):
    template_name = 'waiters/table_details.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order = Orders.objects.filter(table_id=kwargs['pk']).filter(status=False).prefetch_related('orderdetails_set')

        cat_id = self.request.GET.get('category')
        searched_item_string = self.request.GET.get('item')
        if searched_item_string:
            searched_items = FoodAndDrinks.objects.filter(name__icontains=searched_item_string)
            context['searched_items'] = searched_items
        # order form data
        waiter = self.request.user
        table = Tables.objects.filter(id=self.kwargs['pk'])
        data = {'waiter': waiter,
                'table': table[0]}
        order_form = CreateOrderForm(initial=data)
        context['order_form'] = order_form

        context['user'] = self.request.user
        if order:
            # order details_data data
            order_details_data = {
                'order': order[0],
            }
            order_details_form = CreateOrderDetailsForm(initial=order_details_data)
            context['order_details_form'] = order_details_form
            context['order'] = order[0]
            ordered_items = order[0].orderdetails_set.all()
            context['total_sum'] = sum([item.total_price() for item in ordered_items if item.completed==True])
            sent_items_id = OrderDetails.objects.filter(order=order[0]).filter(completed=True).values('id')
            context['sent_items'] = [item['id'] for item in sent_items_id]

        context['categories'] = Categories.objects.all()
        context['items'] = FoodAndDrinks.objects.filter(category_id=cat_id)
        return context

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.id})


class StartOrder(WaitersAccess, CreateView):
    template_name = 'waiters/new_order.html'
    model = Orders
    form_class = CreateOrderForm

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.table.id})


class AddItemInTheOrder(WaitersAccess, CreateView):
    template_name = 'waiters/add_item.html'
    model = OrderDetails
    form_class = CreateOrderDetailsForm

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.order.table.id})


@group_required(allowed_roles=['Waiters'])
def remove_item(request, pk, *args, **kwargs):
    item = OrderDetails.objects.get(pk=kwargs.get('item_id'))
    item.delete()
    return redirect('table details', pk)


#@permission_required('Waiters')
@group_required(allowed_roles=['Waiters'])
def complete_order(request, pk):
    print(pk)
    item = Orders.objects.get(pk=pk)
    item.status = True
    item.order_end_date = datetime.now()
    item.save()
    return redirect('tables list')

