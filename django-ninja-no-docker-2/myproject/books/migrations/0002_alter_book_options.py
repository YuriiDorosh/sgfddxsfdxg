# Generated by Django 5.1.1 on 2024-09-22 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="book",
            options={"permissions": [("can_view_book", "Can view book")]},
        ),
    ]
