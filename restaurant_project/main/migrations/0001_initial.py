# Generated by Django 3.2.5 on 2022-04-12 15:24

import cloudinary.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
        ),
        migrations.CreateModel(
            name='FoodAndDrinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('image', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.categories')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('quantity', models.FloatField(default=0)),
                ('unit', models.CharField(max_length=10)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('max_seats', models.IntegerField(default=2, validators=[django.core.validators.MinValueValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_start_date', models.DateTimeField(auto_now_add=True)),
                ('order_end_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.tables')),
                ('waiter', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcs', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)])),
                ('completed', models.BooleanField(default=False)),
                ('food_and_drinks', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='main.foodanddrinks')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.orders')),
            ],
        ),
        migrations.CreateModel(
            name='FoodAndDrinksToIngredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('food_and_drinks', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.foodanddrinks')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.ingredients')),
            ],
        ),
        migrations.AddField(
            model_name='foodanddrinks',
            name='ingredients',
            field=models.ManyToManyField(through='main.FoodAndDrinksToIngredients', to='main.Ingredients'),
        ),
        migrations.AddField(
            model_name='foodanddrinks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
