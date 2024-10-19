# Generated by Django 5.1.1 on 2024-10-05 17:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="users_wishlist",
            field=models.ManyToManyField(
                blank=True, related_name="user_wishlist", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
