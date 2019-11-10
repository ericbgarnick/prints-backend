# Generated by Django 2.2.7 on 2019-11-10 00:20

from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import prints.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrintSizeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('base_price_cents', models.PositiveIntegerField(blank=True,
                                                                 null=True)),
                ('ship_price_cents', models.PositiveIntegerField(blank=True,
                                                                 null=True)),
                ('size', enumfields.fields.EnumField(enum=prints.models.PrintSize,
                                                     max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Print',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('print_number', models.PositiveIntegerField()),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                            to='catalogs.Photo')),
                ('size_info', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                                                to='prints.PrintSizeInfo')),
            ],
        ),
    ]
