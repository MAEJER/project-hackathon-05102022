# Generated by Django 4.0.4 on 2022-05-15 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_splunkserverclass_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splunkserverclass',
            name='whitelist',
        ),
        migrations.AddField(
            model_name='splunkserverclass',
            name='whitelists',
            field=models.ManyToManyField(related_name='whitelists', to='app.splunkwhitelist'),
        ),
    ]
