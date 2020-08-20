# Generated by Django 3.0.8 on 2020-08-19 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0024_targettracking_target'),
    ]

    operations = [
        migrations.AlterField(
            model_name='targettracking',
            name='farthest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='farthest', to='backend.Activity'),
        ),
        migrations.AlterField(
            model_name='targettracking',
            name='fastest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fastest', to='backend.Activity'),
        ),
        migrations.AlterField(
            model_name='targettracking',
            name='highest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='highest', to='backend.Activity'),
        ),
        migrations.AlterField(
            model_name='targettracking',
            name='longest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='longest', to='backend.Activity'),
        ),
    ]