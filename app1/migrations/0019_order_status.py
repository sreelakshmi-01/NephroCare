# Generated by Django 5.1.7 on 2025-05-15 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0018_order_payment_method_alter_order_razorpay_order_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')], default='Pending', max_length=20),
        ),
    ]
