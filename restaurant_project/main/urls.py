from django.urls import path

from restaurant_project.main.views.generic import HomeView, AboutView, ContactsView, ProjectsView, SignupView

urlpatterns = (
    path('', HomeView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about view'),
    path('contact', ContactsView.as_view(), name='contacts view'),
    path('projects', ProjectsView.as_view(), name='projects view'),
    path('signup', SignupView.as_view(), name='signup view'),
)