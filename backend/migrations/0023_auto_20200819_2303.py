# Generated by Django 3.0.8 on 2020-08-19 22:03

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_auto_20200819_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challengesubscription',
            name='achieved',
        ),
        migrations.RemoveField(
            model_name='challengesubscription',
            name='farthest',
        ),
        migrations.RemoveField(
            model_name='challengesubscription',
            name='fastest',
        ),
        migrations.RemoveField(
            model_name='challengesubscription',
            name='highest',
        ),
        migrations.RemoveField(
            model_name='challengesubscription',
            name='longest',
        ),
        migrations.CreateModel(
            name='TargetTracking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('achieved', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('farthest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='farthest', to='backend.Activity')),
                ('fastest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fastest', to='backend.Activity')),
                ('highest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='highest', to='backend.Activity')),
                ('longest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='longest', to='backend.Activity')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.ChallengeSubscription')),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]