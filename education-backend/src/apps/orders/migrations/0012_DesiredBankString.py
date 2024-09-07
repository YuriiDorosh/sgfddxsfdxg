# Generated by Django 3.1.6 on 2021-02-06 14:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0011_NotificationToGiverIsSent"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="desired_bank",
            field=models.CharField(blank=True, max_length=32, verbose_name="User-requested bank string"),
        ),
    ]
