# Generated by Django 5.1.6 on 2025-03-14 07:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("MainSystem", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="package",
            name="user_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="packages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="store",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="store_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payments",
                to="MainSystem.store",
            ),
        ),
        migrations.AddField(
            model_name="store",
            name="store_category_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="MainSystem.storecategory",
            ),
        ),
        migrations.AddField(
            model_name="theme",
            name="package_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="MainSystem.package",
            ),
        ),
        migrations.AddField(
            model_name="store",
            name="themes",
            field=models.ManyToManyField(to="MainSystem.theme"),
        ),
    ]
