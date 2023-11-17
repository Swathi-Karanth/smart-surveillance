# Generated by Django 4.2.7 on 2023-11-16 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="duty_roster",
            name="SHIFT",
            field=models.ForeignKey(
                db_column="SHIFT_ID",
                on_delete=django.db.models.deletion.CASCADE,
                to="website.shift_master",
            ),
        ),
        migrations.AlterField(
            model_name="duty_roster",
            name="STAFF",
            field=models.ForeignKey(
                db_column="STAFF_ID",
                on_delete=django.db.models.deletion.CASCADE,
                to="website.staff_master",
            ),
        ),
    ]