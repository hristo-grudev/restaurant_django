from django.contrib import admin

from restaurant_project.main.models import Tables, Orders, OrderDetails, Ingredients, Categories, \
    FoodAndDrinksToIngredients, FoodAndDrinks


@admin.register(Tables)
class TablesToIngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(Orders)
class OrdersToIngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetails)
class OrderDetailsToIngredientsAdmin(admin.ModelAdmin):
    pass


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
