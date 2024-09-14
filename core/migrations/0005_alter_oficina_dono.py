# Generated by Django 5.1 on 2024-09-06 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_alter_nota_parcelas"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="oficina",
            name="dono",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="oficina",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
