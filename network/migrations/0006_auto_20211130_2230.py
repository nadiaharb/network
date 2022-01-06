# Generated by Django 3.2.6 on 2021-11-30 18:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20211130_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='subscription',
        ),
        migrations.AddField(
            model_name='following',
            name='subscription',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='subs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='following',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
