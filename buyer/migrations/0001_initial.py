# Generated by Django 2.1.7 on 2021-05-18 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ecommerce', '0001_initial'),
        ('seller', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address_line1', models.CharField(max_length=100)),
                ('Address_line2', models.CharField(max_length=100)),
                ('pincode', models.IntegerField()),
                ('city', models.CharField(max_length=100)),
                ('landmark', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=13)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.userProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.userProfile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('order_date', models.DateField(auto_now=True)),
                ('total_amt', models.DecimalField(decimal_places=3, max_digits=10)),
                ('amt_status', models.IntegerField(default=0)),
                ('Address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyer.AddressDetails')),
                ('placed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.userProfile')),
            ],
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buyer.orders'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.Product'),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'product')},
        ),
    ]
