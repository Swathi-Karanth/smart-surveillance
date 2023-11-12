# Generated by Django 4.2.6 on 2023-11-12 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="staff_master_view",
            fields=[
                ("STAFF_ID", models.AutoField(primary_key=True, serialize=False)),
                ("STAFF_NAME", models.CharField(max_length=255)),
                (
                    "USERNAME",
                    models.CharField(
                        default="<django.db.models.fields.AutoField>", max_length=100
                    ),
                ),
                ("GENDER", models.CharField(max_length=1)),
                ("DOB", models.DateField()),
                ("MOBILE_NO", models.CharField(max_length=20)),
                ("EMAIL_ID", models.CharField(db_column="EMAIL_ID", max_length=20)),
                ("JOINING_DATE", models.DateField()),
                ("LEAVING_DATE", models.DateField()),
                ("ACTIVE_STATUS", models.CharField(default="A", max_length=1)),
                ("EMPLOYEE_ID", models.CharField(max_length=20)),
                ("PASSWORD", models.CharField(db_column="PASSWORD", max_length=20)),
                ("STAFF_ROLE_ID", models.IntegerField()),
                ("ROLE_NAME", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "staff_master_view",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="audit_change_history",
            fields=[
                ("audit_id", models.AutoField(primary_key=True, serialize=False)),
                ("parent_table_pk", models.BigIntegerField()),
                ("old_row_data", models.JSONField(blank=True, null=True)),
                ("new_row_data", models.JSONField(blank=True, null=True)),
                ("dml_type", models.CharField(max_length=10)),
                ("dml_timestamp", models.DateTimeField()),
                ("audit_table_name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "audit_change_history",
            },
        ),
        migrations.CreateModel(
            name="cctv",
            fields=[
                ("CCTV_ID", models.AutoField(primary_key=True, serialize=False)),
                ("CCTV_LOCATION", models.CharField(max_length=50)),
                ("MODEL", models.CharField(max_length=50)),
                ("FOLDER", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "cctv",
            },
        ),
        migrations.CreateModel(
            name="EMERGENCY_CONTACTS",
            fields=[
                (
                    "e_id",
                    models.AutoField(
                        db_column="e_id", primary_key=True, serialize=False
                    ),
                ),
                ("type", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=200)),
                ("contact_no", models.CharField(max_length=20)),
                ("google_map_link", models.CharField(max_length=1000)),
            ],
            options={
                "db_table": "EMERGENCY_CONTACTS",
            },
        ),
        migrations.CreateModel(
            name="incident_types",
            fields=[
                ("INC_TYPE_ID", models.AutoField(primary_key=True, serialize=False)),
                ("INCIDENT_TYPE", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "incident_types",
            },
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=15)),
                ("address", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=50)),
                ("state", models.CharField(max_length=50)),
                ("zipcode", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                ("role_id", models.AutoField(primary_key=True, serialize=False)),
                ("role_name", models.CharField(max_length=20)),
            ],
            options={
                "db_table": "roles",
            },
        ),
        migrations.CreateModel(
            name="shift_master",
            fields=[
                ("SHIFT_ID", models.AutoField(primary_key=True, serialize=False)),
                ("SHIFT_NAME", models.CharField(max_length=255)),
                ("START_TIME", models.CharField(max_length=50)),
                ("END_TIME", models.CharField(max_length=50)),
            ],
            options={
                "db_table": "SHIFT_MASTER",
            },
        ),
        migrations.CreateModel(
            name="staff_master",
            fields=[
                ("STAFF_ID", models.AutoField(primary_key=True, serialize=False)),
                ("STAFF_NAME", models.CharField(max_length=255)),
                (
                    "USERNAME",
                    models.CharField(
                        default="<django.db.models.fields.AutoField>", max_length=100
                    ),
                ),
                ("GENDER", models.CharField(max_length=1)),
                ("DOB", models.DateField()),
                ("MOBILE_NO", models.CharField(max_length=20)),
                ("EMAIL_ID", models.CharField(db_column="EMAIL_ID", max_length=20)),
                ("JOINING_DATE", models.DateField()),
                ("LEAVING_DATE", models.DateField()),
                ("ACTIVE_STATUS", models.CharField(default="A", max_length=1)),
                ("EMPLOYEE_ID", models.CharField(max_length=20)),
                ("PASSWORD", models.CharField(db_column="PASSWORD", max_length=20)),
                (
                    "STAFF_ROLE",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.roles"
                    ),
                ),
            ],
            options={
                "db_table": "staff_master",
            },
        ),
        migrations.CreateModel(
            name="visitor_ledger",
            fields=[
                ("VISITOR_ID", models.AutoField(primary_key=True, serialize=False)),
                ("DATE_TIME", models.DateTimeField(auto_now_add=True)),
                ("VISITOR_NAME", models.CharField(max_length=100)),
                ("PURPOSE_OF_VISIT", models.CharField(max_length=100)),
                ("ENTRY_DATE_TIME", models.DateTimeField()),
                ("EXIT_DATE_TIME", models.DateTimeField()),
                ("VISITOR_CONTACT", models.CharField(max_length=20)),
                (
                    "RECORDED_BY",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.staff_master",
                    ),
                ),
            ],
            options={
                "db_table": "visitor_ledger",
            },
        ),
        migrations.CreateModel(
            name="incidents",
            fields=[
                (
                    "INCIDENT_ID",
                    models.AutoField(
                        db_column="INCIDENT_ID", primary_key=True, serialize=False
                    ),
                ),
                ("INCIDENT_DESC", models.CharField(max_length=500)),
                ("REPORTED_DATE_TIME", models.DateTimeField()),
                ("ACTION", models.CharField(max_length=500)),
                ("STATUS", models.CharField(max_length=1)),
                (
                    "INCIDENT_TYPE",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.incident_types",
                    ),
                ),
                (
                    "REPORTED_STAFF",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.staff_master",
                    ),
                ),
            ],
            options={
                "db_table": "incidents",
            },
        ),
        migrations.CreateModel(
            name="footage_view",
            fields=[
                ("FOOTAGE_ID", models.AutoField(primary_key=True, serialize=False)),
                ("START_TIMESTAMP", models.TimeField()),
                ("END_TIMESTAMP", models.TimeField()),
                ("video_folder", models.CharField(max_length=50)),
                ("FOLDER", models.CharField(max_length=50)),
                (
                    "CCTV_ID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.cctv"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="footage",
            fields=[
                ("FOOTAGE_ID", models.AutoField(primary_key=True, serialize=False)),
                ("START_TIMESTAMP", models.TimeField()),
                ("END_TIMESTAMP", models.TimeField()),
                ("video_folder", models.CharField(max_length=50)),
                (
                    "CCTV_ID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="website.cctv"
                    ),
                ),
            ],
            options={
                "db_table": "footage",
            },
        ),
        migrations.CreateModel(
            name="duty_roster",
            fields=[
                (
                    "STAFF_SHIFT",
                    models.AutoField(
                        db_column="STAFF_SHIFT_ID", primary_key=True, serialize=False
                    ),
                ),
                ("START_DATE_TIME", models.DateTimeField()),
                ("END_DATE_TIME", models.DateTimeField()),
                (
                    "SHIFT",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.shift_master",
                    ),
                ),
                (
                    "STAFF",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="website.staff_master",
                    ),
                ),
            ],
            options={
                "db_table": "DUTY_ROSTER",
            },
        ),
    ]
