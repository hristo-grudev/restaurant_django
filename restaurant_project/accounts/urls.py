from django.urls import path

from restaurant_project.accounts.views import UserRegisterView, UserLoginView, UserDetailsView, EditProfileView, \
    ChangeUserPasswordView, UserLogoutView, PasswordChangeDone

urlpatterns = (
    path('register/', UserRegisterView.as_view(), name='register user'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', UserLogoutView.as_view(), name='logout user'),
    path('profile/<int:pk>/', UserDetailsView.as_view(), name='details profile'),
    path('edit-profile/<int:pk>/', EditProfileView.as_view(), name='edit profile'),
    path('edit-profile/password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', PasswordChangeDone.as_view(), name='password_change_done'),
)
