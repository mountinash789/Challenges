# Generated by Django 3.0.8 on 2021-03-07 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['created']},
        ),
        migrations.AddField(
            model_name='tag',
            name='text_color',
            field=models.CharField(default='1', max_length=255),
            preserve_default=False,
        ),
    ]
