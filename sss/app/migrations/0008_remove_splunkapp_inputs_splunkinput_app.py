# Generated by Django 4.0.4 on 2022-05-15 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_splunkinput_splunkapp_inputs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splunkapp',
            name='inputs',
        ),
        migrations.AddField(
            model_name='splunkinput',
            name='app',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='app', to='app.splunkapp'),
        ),
    ]