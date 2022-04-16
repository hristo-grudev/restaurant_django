from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, RedirectView

from restaurant_project.accounts.forms import CreateProfileForm, EditProfileForm, PasswordChangingForm
from restaurant_project.accounts.models import Profile

user_model = get_user_model()


class UserRegisterView(CreateView):
    form_class = CreateProfileForm
    template_name = 'accounts/profile_create.html'
    success_url = reverse_lazy('index')


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('index')

    def get_success_url(self):
        if self.request.user.groups.all()[0].name in ['Cooks', 'Bartenders']:
            self.success_url = reverse_lazy('kitchen home view')
        if self.request.user.groups.all()[0].name in ['Waiters']:
            self.success_url = reverse_lazy('tables list')
        if self.request.user.groups.all()[0].name in ['Customers']:
            self.success_url = reverse_lazy('menu view', args=(1,))
        if self.success_url:
            return self.success_url
        return super().get_success_url()


class UserDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile_details.html'
    context_object_name = 'profile'


class EditProfileView(UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    form_class = EditProfileForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.id != kwargs['pk']:
            return redirect('details profile', self.request.user.id)

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('details profile', args=(self.request.user.id,))


class ChangeUserPasswordView(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDone(RedirectView):
    password_success_message = 'Паролата е променена успешно.'

    def get_redirect_url(self, *args, **kwargs):
        messages.success(self.request, self.password_success_message)
        return reverse_lazy('details profile', kwargs={"pk":self.request.user.id})

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(settings.LOGIN_URL)
