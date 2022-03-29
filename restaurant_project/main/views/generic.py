from django.views.generic import TemplateView, ListView

from restaurant_project.kitchen.models import FoodAndDrinks, Categories


class HomeView(TemplateView):
    template_name = 'main/home_page.html'


class ContactsView(TemplateView):
    template_name = 'main/contact_page.html'


class MenuView(ListView):
    template_name = 'main/menu_page.html'
    model = FoodAndDrinks

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = Categories.objects.all()

        context['categories'] = categories

        return context

    def get_queryset(self):
        return super()\
            .get_queryset()\
            .filter(category_id=self.kwargs['pk'])
