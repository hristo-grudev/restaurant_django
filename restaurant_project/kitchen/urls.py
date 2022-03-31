from django.urls import path

from restaurant_project.kitchen.views import KitchenHomeView, ItemEditView, ItemCreateView, complete_item, EditMenuView, \
    remove_ingredient, add_ingredient_view

urlpatterns = (
    path('', KitchenHomeView.as_view(), name='kitchen home view'),
    path('create', ItemCreateView.as_view(), name='item create view'),
    path('edit/<int:pk>/', ItemEditView.as_view(), name='item edit view'),
    path('complete/<int:pk>/', complete_item, name='complete item view'),
    path('menu/<int:pk>/', EditMenuView.as_view(), name='edit menu view'),
    path('edit/<int:pk>/<int:ingredient_id>/', remove_ingredient, name='remove ingredient view'),
    path('edit/<int:pk>/add-ingredient/', add_ingredient_view, name='add ingredient view'),

)
