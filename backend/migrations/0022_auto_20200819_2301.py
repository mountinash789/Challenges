# Generated by Django 3.0.8 on 2020-08-19 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0021_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='pace',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='challengesubscription',
            name='achieved',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='challengesubscription',
            name='farthest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farthest', to='backend.Activity'),
        ),
        migrations.AddField(
            model_name='challengesubscription',
            name='fastest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fastest', to='backend.Activity'),
        ),
        migrations.AddField(
            model_name='challengesubscription',
            name='highest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest', to='backend.Activity'),
        ),
        migrations.AddField(
            model_name='challengesubscription',
            name='longest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='longest', to='backend.Activity'),
        ),
    ]
