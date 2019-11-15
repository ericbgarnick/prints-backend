# Generated by Django 2.2.7 on 2019-11-15 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geospatial', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=128)),
                ('phone', models.CharField(blank=True, max_length=12, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='geospatial.Address')),
            ],
        ),
    ]
