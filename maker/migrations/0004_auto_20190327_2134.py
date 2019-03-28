# Generated by Django 2.1.1 on 2019-03-28 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maker', '0003_remove_cryptocurrency_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='time',
            field=models.ManyToManyField(through='maker.Metric', to='maker.Timeslot'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='crypto_currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.CryptoCurrency'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='timeslot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.Timeslot'),
        ),
    ]
