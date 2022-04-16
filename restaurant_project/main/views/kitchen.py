from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, TemplateView, ListView

from restaurant_project.common.helpers import group_required
from restaurant_project.common.view_mixins import BarAndKitchenAccess
from restaurant_project.main.forms.kitchen_forms import EditItemFrom, CreateItemFrom, AddIngredientForm
from restaurant_project.main.models import FoodAndDrinks, Ingredients, Categories, FoodAndDrinksToIngredients
from restaurant_project.main.models import Orders, OrderDetails


class KitchenHomeView(BarAndKitchenAccess, TemplateView):
    template_name = 'kitchen/kitchen_home.html'
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_group_all = self.request.user.groups.all()
        user_group = user_group_all[0]
        order_items = OrderDetails.objects.filter(completed=False).filter(food_and_drinks__category__group=user_group)
        context['order_items'] = order_items
        context['user_group'] = user_group

        return context

    def get_success_url(self):
        return reverse_lazy('kitchen home view')


class ItemEditView(BarAndKitchenAccess, UpdateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_edit.html'
    form_class = EditItemFrom

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        searched_item_string = self.request.GET.get('item')
        if searched_item_string:
            searched_items = FoodAndDrinksToIngredients.objects.filter(ingredient__name__contains=searched_item_string)
            context['searched_items'] = searched_items

        current_ingredient = FoodAndDrinksToIngredients.objects.filter(food_and_drinks=self.object.id)
        context['current_ingredient'] = current_ingredient
        ingredient_form = AddIngredientForm
        context['ingredient_form'] = ingredient_form

        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


    def get_success_url(self):
        return reverse_lazy('edit menu view', kwargs={'pk': self.object.category.id})


class ItemCreateView(BarAndKitchenAccess, CreateView):
    model = FoodAndDrinks
    template_name = 'kitchen/item_create.html'
    form_class = CreateItemFrom
    success_url = reverse_lazy('kitchen home view')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@group_required(allowed_roles=['Cooks', 'Bartenders'])
def complete_item(request, pk):
    item = OrderDetails.objects.get(pk=pk)
    item.completed = True
    ingredients = item.food_and_drinks.foodanddrinkstoingredients_set.all()
    for ingr in ingredients:
        ingredient = Ingredients.objects.get(pk=ingr.ingredient.id)
        ingredient.quantity -= ingr.quantity
        ingredient.save()

    item.save()
    return redirect('kitchen home view')


class EditMenuView(BarAndKitchenAccess, ListView):
    template_name = 'kitchen/menu_edit.html'
    model = FoodAndDrinks

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        categories = Categories.objects.filter(group=self.request.user.groups.all()[0])

        context['categories'] = categories

        return context

    def get_queryset(self):
        return super() \
            .get_queryset() \
            .filter(category_id=self.kwargs['pk']) \
            .filter(user=self.request.user)

@group_required(allowed_roles=['Cooks', 'Bartenders'])
def remove_ingredient(request, pk, *args, **kwargs):
    item = FoodAndDrinksToIngredients.objects.get(pk=kwargs.get('ingredient_id'))
    item.delete()
    return redirect('item edit view', pk)

@group_required(allowed_roles=['Cooks', 'Bartenders'])
def add_ingredient_view(request, pk, *args, **kwargs):
    value_error_message = 'Quantity must be positive number.'
    if request.method == 'POST':
        ingredient = Ingredients.objects.get(id=request.POST['ingredient'])
        food_and_drinks = FoodAndDrinks.objects.get(id=pk)
        quantity = request.POST['quantity']
        food_ingredient = FoodAndDrinksToIngredients.objects.get_or_create(
            ingredient=ingredient,
            food_and_drinks=food_and_drinks,
        )
        if float(quantity) < 0:
            raise ValueError(value_error_message)
        food_ingredient[0].quantity = quantity
        food_ingredient[0].save()

    return redirect('item edit view', pk)


class IngredientsView(BarAndKitchenAccess, ListView):
    model = Ingredients
    template_name = 'kitchen/ingredients.html'
    paginate_by = 10