# Generated by Django 5.1.7 on 2025-03-30 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_dialysiscenter'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hosp_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255, null=True)),
                ('district', models.CharField(max_length=255)),
                ('phone_no', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]
