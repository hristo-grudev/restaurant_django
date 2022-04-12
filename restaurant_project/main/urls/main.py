from django.urls import path

from restaurant_project.main.views.generic import HomeView, ContactsView, MenuView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('contacts/', ContactsView.as_view(), name='contacts view'),
    path('menu/<int:pk>/', MenuView.as_view(), name='menu view'),
)
