# Generated by Django 3.0.8 on 2020-08-02 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20200801_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='class_str',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='connection',
            name='library',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
