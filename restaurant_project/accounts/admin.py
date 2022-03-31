from django.contrib import admin

from restaurant_project.accounts.models import RestaurantUser, Profile


@admin.register(RestaurantUser)
class RestaurantUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass