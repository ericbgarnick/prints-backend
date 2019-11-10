# Generated by Django 2.2.7 on 2019-11-10 18:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('publish_date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('image_id', models.PositiveIntegerField(primary_key=True,
                                                         serialize=False)),
                ('image_location', models.ImageField(upload_to='photos')),
                ('title', models.CharField(max_length=256)),
                ('shot_date', models.DateField()),
                ('max_prints', models.PositiveIntegerField()),
                ('catalog', models.ForeignKey(blank=True, null=True,
                                              on_delete=django.db.models.deletion.SET_NULL,
                                              to='catalog.Catalog')),
            ],
        ),
    ]
