# Generated by Django 5.1 on 2024-09-06 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_alter_imagem_id_alter_link_id_alter_nota_id_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="nota",
            name="cliente",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="notas",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
