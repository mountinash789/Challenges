# Generated by Django 3.0.8 on 2020-10-03 23:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0005_auto_20201004_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='dessert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Dessert'),
        ),
        migrations.AddField(
            model_name='guest',
            name='main',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Main'),
        ),
        migrations.AddField(
            model_name='guest',
            name='starter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Starter'),
        ),
    ]