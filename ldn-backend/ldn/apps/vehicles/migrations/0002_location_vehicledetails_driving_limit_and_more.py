# Generated by Django 4.0.2 on 2023-05-08 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=200, verbose_name='City Name')),
            ],
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='driving_limit',
            field=models.IntegerField(default=1, verbose_name='Driving Limit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='location_area',
            field=models.BooleanField(default=False, verbose_name='Inside Area'),
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='security_deposit',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=6, verbose_name='Security Deposit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehicledetails',
            name='vehicle_location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='vehicles.location', verbose_name='Vehicle Location'),
            preserve_default=False,
        ),
    ]