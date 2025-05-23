# Generated by Django 5.2 on 2025-05-21 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('checkout', '0002_orderitem_product_detail'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShippingAddress',
            new_name='Address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='shipping_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_price',
            new_name='total_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='paid_at',
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(max_length=50),
        ),
    ]
