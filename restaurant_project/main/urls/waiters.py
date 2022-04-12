from django.urls import path

from restaurant_project.main.views.waiters import TablesView, TableDetailsView, StartOrder, AddItemInTheOrder, remove_item, \
    complete_order

urlpatterns = (
    path('', TablesView.as_view(), name='tables list'),
    path('<int:pk>/', TableDetailsView.as_view(), name='table details'),
    path('<int:pk>/new-order/', StartOrder.as_view(), name = 'order start'),
    path('<int:pk>/add-item/', AddItemInTheOrder.as_view(), name='order add item'),
    path('<int:pk>/complete/', complete_order, name='complete order'),
    path('<int:pk>/<int:item_id>/', remove_item, name='remove item'),
)
