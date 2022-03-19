from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DeleteView

from restaurant_project.kitchen.forms import CreateOrderForm, CreateOrderDetailsForm, DeleteOrderDetailsForm
from restaurant_project.kitchen.models import Categories, FoodAndDrinks
from restaurant_project.waiters.models import Tables, Orders, OrderDetails


class TablesView(ListView):
    template_name = 'waiters/tables_page.html'
    model = Tables

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        orders_data = Orders.objects.filter(status=False)
        context['tables'] = Tables.objects.all()
        context['occupied_table'] = [order.table_id for order in orders_data]

        return context


class TableDetailsView(TemplateView):
    template_name = 'waiters/table_details.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        order = Orders.objects.filter(table_id=kwargs['pk']).filter(status=False)

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
            context['order'] = order
            context['ordered_items'] = OrderDetails.objects.filter(order=order[0])
            sent_items_id = OrderDetails.objects.filter(order=order[0]).filter(completed=True).values('id')
            context['sent_items'] = [item['id'] for item in sent_items_id]
            context['delete_from'] = DeleteOrderDetailsForm
            print(context['sent_items'])

        context['categories'] = Categories.objects.all()
        context['items'] = FoodAndDrinks.objects.filter(category_id=cat_id)
        return context

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.id})


class StartOrder(CreateView):
    template_name = 'waiters/new_order.html'
    model = Orders
    form_class = CreateOrderForm

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.table.id})


class AddItemInTheOrder(CreateView):
    template_name = 'waiters/add_item.html'
    model = OrderDetails
    form_class = CreateOrderDetailsForm

    def get_success_url(self):
        return reverse_lazy('table details', kwargs={'pk': self.object.order.table.id})



class RemoveItemView(DeleteView):
    model = OrderDetails
    template_name = 'waiters/remove_item.html'
    form_class = DeleteOrderDetailsForm

    def get_success_url(self):
        # return reverse_lazy('table list')
        return reverse_lazy('table details', kwargs={'pk': self.kwargs.get('pk')})

    def get_object(self):
        object = get_object_or_404(OrderDetails, id=self.kwargs.get('item_id'))
        print(object)
        return get_object_or_404(OrderDetails, id=self.kwargs.get('item_id'))