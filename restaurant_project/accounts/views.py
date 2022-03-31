from django.conf import settings
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView

from restaurant_project.accounts.forms import CreateProfileForm

user_model = get_user_model()

class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('index')


class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.request.user.groups.all()[0].name in ['Cooks', 'Bartenders']:
            self.success_url = reverse_lazy('kitchen home view')
        if self.request.user.groups.all()[0].name in ['Waiters']:
            self.success_url = reverse_lazy('tables list')
        if self.request.user.groups.all()[0].name in ['Customers']:
            self.success_url = reverse_lazy('menu view')
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserDetailsView(DetailView):
    model = user_model
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class EditProfileView:
    pass


class ChangeUserPasswordView:
    pass


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
