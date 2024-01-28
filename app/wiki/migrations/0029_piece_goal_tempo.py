# Generated by Django 4.2.9 on 2024-01-28 03:24

import wiki.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wiki", "0028_piece_measures"),
    ]

    operations = [
        migrations.AddField(
            model_name="piece",
            name="goal_tempo",
            field=models.IntegerField(
                blank=True, null=True, validators=[wiki.models.validate_positive]
            ),
        ),
    ]