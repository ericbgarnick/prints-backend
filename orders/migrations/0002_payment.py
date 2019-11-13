# Generated by Django 2.2.7 on 2019-11-13 02:25

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('geospatial', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', enumfields.fields.EnumField(enum=orders.models.PaymentMethod, max_length=8)),
                ('credit_network', enumfields.fields.EnumField(enum=orders.models.CreditNetwork, max_length=16, null=True)),
                ('account_number', models.CharField(max_length=20)),
                ('card_expiration', models.CharField(max_length=6)),
                ('card_cvv', models.CharField(max_length=8)),
                ('billing_name', models.CharField(max_length=128)),
                ('billing_address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geospatial.Address')),
            ],
        ),
    ]
