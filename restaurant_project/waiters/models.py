from django.core.validators import MinValueValidator
from django.db import models

from restaurant_project.accounts.models import RestaurantUser
from restaurant_project.kitchen.models import FoodAndDrinks


class Tables(models.Model):
    TABLE_MAX_LENGTH = 25
    TABLE_MIN_SEAT = 2

    name = models.CharField(
        max_length=TABLE_MAX_LENGTH,
    )

    max_seats = models.IntegerField(
        default=TABLE_MIN_SEAT,
        validators=(
            MinValueValidator(TABLE_MIN_SEAT),
        )
    )

    def __str__(self):
        return f'Table: {self.name}'


class Orders(models.Model):
    order_start_date = models.DateTimeField(
        auto_now_add=True,
    )

    order_end_date = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.BooleanField(
        default=False,
    )

    table = models.ForeignKey(
        Tables,
        on_delete=models.DO_NOTHING,
    )

    waiter = models.ForeignKey(
        RestaurantUser,
        on_delete=models.DO_NOTHING,
    )


class OrderDetails(models.Model):
    PCS_MIN_VALUE = 0.0
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
    )
    food_and_drinks = models.ForeignKey(
        FoodAndDrinks,
        on_delete=models.DO_NOTHING,
    )

    pcs = models.FloatField(
        validators=(
            MinValueValidator(PCS_MIN_VALUE),
        )
    )

    completed = models.BooleanField(
        default=False
    )

    def total_price(self):
        return self.pcs * self.food_and_drinks.price
