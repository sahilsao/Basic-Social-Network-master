# Generated by Django 3.0.7 on 2020-08-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0006_auto_20200809_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='total_likes',
            field=models.IntegerField(default=0),
        ),
    ]
