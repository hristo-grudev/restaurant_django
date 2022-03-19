from django.contrib import admin

from restaurant_project.waiters.models import Tables, Orders, OrderDetails


@admin.register(Tables)
class TablesToIngredientsAdmin(admin.ModelAdmin):
    pass

@admin.register(Orders)
class OrdersToIngredientsAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderDetails)
class OrderDetailsToIngredientsAdmin(admin.ModelAdmin):
    pass
