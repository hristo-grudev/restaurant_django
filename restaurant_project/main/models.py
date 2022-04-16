from cloudinary import models as cloudinary_models
from django.contrib.auth.models import Group
from django.core.validators import MinValueValidator
from django.db import models

from restaurant_project.accounts.models import RestaurantUser


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
        return f'Маса: {self.name}'


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

    class Meta:
        ordering = ['name']


class Categories(models.Model):
    CATEGORY_MAX_LENGTH = 30

    name = models.CharField(
        max_length=CATEGORY_MAX_LENGTH,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class FoodAndDrinks(models.Model):
    FOOD_AND_DRINKS_NAME_MAX_LENGTH = 50
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

    image = cloudinary_models.CloudinaryField('image', blank=True, null=True)

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
        validators=(
            MinValueValidator(QUANTITY_MIN_VALUE),
        )
    )

    def __str__(self):
        return self.food_and_drinks.name


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

    def __str__(self):
        return f'Table: {self.table.name}'

    class Meta:
        ordering = ['pk']


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

    def __str__(self):
        return self.food_and_drinks.name
