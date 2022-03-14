from django.urls import path

from restaurant_project.waiters.views import TablesView, TableDetailsView

urlpatterns = (
    path('', TablesView.as_view(), name='tables list'),
    path('<int:pk>/', TableDetailsView.as_view(), name='table details')
)