from django.contrib import admin

from restaurant_project.accounts.models import RestaurantUser


@admin.register(RestaurantUser)
class RestaurantUserAdmin(admin.ModelAdmin):
    pass