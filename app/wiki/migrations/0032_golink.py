# Generated by Django 4.2.9 on 2024-12-30 22:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wiki", "0031_delete_golink"),
    ]

    operations = [
        migrations.CreateModel(
            name="GoLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slug", models.CharField(max_length=255)),
                ("endpoint", models.CharField(max_length=255)),
            ],
        ),
    ]
