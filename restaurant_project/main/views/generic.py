from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/home_page.html'

class AboutView(TemplateView):
    template_name = 'main/about_page.html'

class ContactsView(TemplateView):
    template_name = 'main/contact_page.html'

class ProjectsView(TemplateView):
    template_name = 'waiters/tables_page.html'

class SignupView(TemplateView):
    template_name = 'main/signup_page.html'

