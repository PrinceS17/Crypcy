# Generated by Django 2.1.1 on 2019-04-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190416_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='favorite',
            field=models.ManyToManyField(blank=True, to='maker.CryptoCurrency'),
        ),
    ]
