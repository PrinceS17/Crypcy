# Generated by Django 2.1.1 on 2019-04-08 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='score_of_knowledge',
            field=models.FloatField(blank=True, default=None, null=True, verbose_name='score of knowledge'),
        ),
    ]
