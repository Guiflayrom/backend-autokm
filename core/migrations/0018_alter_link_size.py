# Generated by Django 5.1 on 2024-09-16 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_alter_link_file_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="size",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
