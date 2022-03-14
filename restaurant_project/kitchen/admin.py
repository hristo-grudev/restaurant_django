from django.contrib import admin

from restaurant_project.kitchen.models import Ingredients, Categories, FoodAndDrinks, FoodAndDrinksToIngredients


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(FoodAndDrinks)
class FoodAndDrinksAdmin(admin.ModelAdmin):
    pass


@admin.register(FoodAndDrinksToIngredients)
class FoodAndDrinksToIngredientsAdmin(admin.ModelAdmin):
    pass
