# Generated by Django 4.2.9 on 2024-01-26 00:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wiki", "0025_alter_step_order"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Step",
        ),
    ]
