from django.urls import path

from restaurant_project.kitchen.views import KitchenHomeView, ItemEditView, ItemCreateView

urlpatterns = (
    path('', KitchenHomeView.as_view(), name='kitchen home view'),
    path('create', ItemCreateView.as_view(), name='item create view'),
    path('edit/<int:pk>', ItemEditView.as_view(), name='item edit view'),

)
