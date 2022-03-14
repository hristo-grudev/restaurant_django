from django.core.validators import MinValueValidator
from django.db import models

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

class Orders(models.Model):
    food_and_drinks = models.ForeignKey(
        FoodAndDrinks,
        on_delete=models.DO_NOTHING,
    )
    order_start_date = models.DateTimeField(
        auto_now_add=True,
    )

    order_end_date = models.DateTimeField()

    status = models.BooleanField(
        default=False,
    )

    table = models.ForeignKey(
        Tables,
        on_delete=models.DO_NOTHING,
    )
