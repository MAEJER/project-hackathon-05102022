# Generated by Django 4.0.4 on 2022-05-15 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_splunkfilesha_unique_sha_combination'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerClassApps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ServerClassWhitelists',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SplunkApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='SplunkGitConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repo_name', models.CharField(max_length=128)),
                ('path_name', models.CharField(max_length=256)),
                ('branch', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SplunkHost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='SplunkWhitelist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('hosts', models.ManyToManyField(related_name='hosts', to='app.splunkhost')),
            ],
        ),
        migrations.DeleteModel(
            name='ServerClass',
        ),
        migrations.AddField(
            model_name='serverclasswhitelists',
            name='whitelist',
            field=models.ManyToManyField(related_name='whitelist', to='app.splunkapp'),
        ),
        migrations.AddField(
            model_name='serverclassapps',
            name='apps',
            field=models.ManyToManyField(related_name='apps', to='app.splunkapp'),
        ),
    ]
