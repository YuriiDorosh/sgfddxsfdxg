# Generated by Django 4.1.7 on 2023-04-26 05:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0026_PromocodeExpiration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="promocode",
            name="comment",
            field=models.TextField(default=" ", verbose_name="Destination"),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name="promocode",
            old_name="comment",
            new_name="destination",
        ),
    ]
