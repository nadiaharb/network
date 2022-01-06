# Generated by Django 3.2.6 on 2021-11-30 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subat', models.IntegerField(blank=True, null=True)),
                ('subto', models.IntegerField(blank=True, null=True)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.post')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]