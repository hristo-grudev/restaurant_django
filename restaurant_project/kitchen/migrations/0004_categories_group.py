# Generated by Django 3.2.5 on 2022-03-22 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('kitchen', '0003_categories_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.group'),
            preserve_default=False,
        ),
    ]