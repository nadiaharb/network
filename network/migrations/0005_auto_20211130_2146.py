# Generated by Django 3.2.6 on 2021-11-30 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='subscription',
        ),
        migrations.AddField(
            model_name='following',
            name='subscription',
            field=models.ManyToManyField(to='network.Post'),
        ),
    ]
