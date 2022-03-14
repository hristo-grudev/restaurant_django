from django.core.validators import MinValueValidator
from django.db import models

from restaurant_project.accounts.models import RestaurantUser


class Ingredients(models.Model):
    INGREDIENTS_NAME_MAX_LENGTH = 30
    INGREDIENTS_UNIT_MAX_LENGTH = 10

    name = models.CharField(
        max_length=INGREDIENTS_NAME_MAX_LENGTH,
        unique=True,
    )

    quantity = models.FloatField(
        default=0,
    )

    unit = models.CharField(
        max_length=INGREDIENTS_UNIT_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class Categories(models.Model):
    CATEGORY_MAX_LENGTH = 30

    name = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
    )

    image = models.ImageField(
    )

    def __str__(self):
        return self.name


class FoodAndDrinks(models.Model):
    FOOD_AND_DRINKS_NAME_MAX_LENGTH = 30
    MIN_PRICE_VALUE = 0.0
    name = models.CharField(
        max_length=FOOD_AND_DRINKS_NAME_MAX_LENGTH,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.CASCADE,
    )
    price = models.FloatField(
        validators=(
            MinValueValidator(MIN_PRICE_VALUE),
        )
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    image = models.ImageField(
    )

    user = models.ForeignKey(
        RestaurantUser,
        on_delete=models.DO_NOTHING,
    )

    ingredients = models.ManyToManyField(
        Ingredients,
        through='FoodAndDrinksToIngredients'
    )

    def __str__(self):
        return self.name

class FoodAndDrinksToIngredients(models.Model):
    QUANTITY_MIN_VALUE = 0.0

    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
    )
    food_and_drinks = models.ForeignKey(
        FoodAndDrinks,
        on_delete=models.CASCADE,
    )
    quantity = models.FloatField(
        default=0,
        validators= (
            MinValueValidator(QUANTITY_MIN_VALUE),
        )
    )

    def __str__(self):
        return self.food_and_drinks.name