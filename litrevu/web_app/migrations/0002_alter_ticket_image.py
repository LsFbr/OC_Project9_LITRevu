# Generated by Django 5.2.4 on 2025-07-25 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="tickets_images/"),
        ),
    ]
