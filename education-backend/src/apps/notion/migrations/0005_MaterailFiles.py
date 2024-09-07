# Generated by Django 4.1.7 on 2023-05-14 17:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notion", "0004_NotionMaterialSlug"),
    ]

    operations = [
        migrations.CreateModel(
            name="MaterialFile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified", models.DateTimeField(blank=True, db_index=True, null=True)),
                ("file", models.FileField(unique=True, upload_to="materials")),
            ],
            options={
                "verbose_name": "Material file",
                "verbose_name_plural": "Material files",
            },
        ),
    ]
