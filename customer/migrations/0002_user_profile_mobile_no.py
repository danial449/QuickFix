# Generated by Django 4.2.11 on 2024-03-12 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user_profile",
            name="mobile_no",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
