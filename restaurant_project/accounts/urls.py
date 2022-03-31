from django.urls import path

from restaurant_project.accounts.views import UserRegisterView, UserLoginView, UserDetailsView, EditProfileView, \
    ChangeUserPasswordView, UserLogoutView

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', UserDetailsView.as_view(), name='details user'),
    # path('edit-profile/<int:pk>/', EditProfileView.as_view(), name='create user'),
    # path('edit-password/<int:pk>/', ChangeUserPasswordView.as_view(), name='create user'),
)
