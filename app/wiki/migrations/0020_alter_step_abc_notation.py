# Generated by Django 4.2.5 on 2023-09-19 21:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wiki", "0019_piece_amazon_music_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="step",
            name="abc_notation",
            field=models.TextField(blank=True, null=True),
        ),
    ]
