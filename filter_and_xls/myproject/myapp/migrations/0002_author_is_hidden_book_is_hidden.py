# Generated by Django 5.1.2 on 2024-10-27 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="author",
            name="is_hidden",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="book",
            name="is_hidden",
            field=models.BooleanField(default=False),
        ),
    ]
