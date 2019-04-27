# Generated by Django 2.1.1 on 2019-04-16 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoCurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('logo', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.IntegerField()),
                ('time', models.DateTimeField(verbose_name='log-in time')),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.PositiveIntegerField()),
                ('privacy', models.FloatField(verbose_name='privacy')),
                ('price', models.FloatField(verbose_name='price')),
                ('supply', models.PositiveIntegerField()),
                ('utility', models.FloatField(verbose_name='utility')),
                ('crypto_currency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.CryptoCurrency')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=200)),
                ('ttype', models.CharField(max_length=200)),
                ('picture', models.URLField()),
                ('content', models.TextField(verbose_name='new content')),
                ('author', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='time slot')),
                ('related_news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.RelatedNews')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('interest_tag', models.CharField(max_length=200)),
                ('score_of_knowledge', models.FloatField(verbose_name='score of knowledge')),
                ('favorite', models.ManyToManyField(to='maker.CryptoCurrency')),
            ],
        ),
        migrations.AddField(
            model_name='metric',
            name='timeslot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.Timeslot'),
        ),
        migrations.AddField(
            model_name='log',
            name='related_news',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.RelatedNews'),
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='maker.User'),
        ),
        migrations.AddField(
            model_name='cryptocurrency',
            name='time',
            field=models.ManyToManyField(through='maker.Metric', to='maker.Timeslot'),
        ),
    ]
