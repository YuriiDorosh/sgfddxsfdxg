# Generated by Django 3.2.8 on 2021-10-17 00:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0014_NonAttachedPromocodes"),
    ]

    operations = [
        migrations.AddField(
            model_name="promocode",
            name="discount_value",
            field=models.IntegerField(help_text="Takes precedence over percent", null=True, blank=True, verbose_name="Discount amount"),
        ),
        migrations.AlterField(
            model_name="promocode",
            name="discount_percent",
            field=models.IntegerField(blank=True, null=True, verbose_name="Discount percent"),
        ),
        migrations.AddConstraint(
            model_name="promocode",
            constraint=models.CheckConstraint(
                check=models.Q(("discount_percent__isnull", False), ("discount_value__isnull", False), _connector="OR"), name="percent or value must be set"
            ),
        ),
    ]
