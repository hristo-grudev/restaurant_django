from django.urls import path

from restaurant_project.waiters.views import TablesView, TableDetailsView, StartOrder, AddItemInTheOrder, RemoveItemView

urlpatterns = (
    path('', TablesView.as_view(), name='tables list'),
    path('<int:pk>/', TableDetailsView.as_view(), name='table details'),
    path('<int:pk>/new-order/', StartOrder.as_view(), name = 'order start'),
    path('<int:pk>/add-item/', AddItemInTheOrder.as_view(), name='order add item'),
    path('<int:pk>/<int:item_id>/', RemoveItemView.as_view(), name='remove item'),
)