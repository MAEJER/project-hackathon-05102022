# Generated by Django 4.0.4 on 2022-05-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_serverclassapps_serverclasswhitelists_splunkapp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SplunkServerClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('apps', models.ManyToManyField(related_name='apps', to='app.splunkapp')),
                ('whitelist', models.ManyToManyField(related_name='whitelist', to='app.splunkwhitelist')),
            ],
        ),
        migrations.RemoveField(
            model_name='serverclasswhitelists',
            name='whitelist',
        ),
        migrations.DeleteModel(
            name='ServerClassApps',
        ),
        migrations.DeleteModel(
            name='ServerClassWhitelists',
        ),
    ]