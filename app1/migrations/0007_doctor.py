# Generated by Django 5.1.7 on 2025-03-31 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_hospital_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('specialization', models.CharField(max_length=255)),
                ('qualification', models.CharField(max_length=255)),
                ('experience', models.PositiveIntegerField(help_text='Years of experience')),
                ('phone_no', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.hospital')),
            ],
        ),
    ]
