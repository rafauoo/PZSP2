# Generated by Django 4.2.6 on 2024-01-12 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_pendingapproval_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='competition',
            name='regulation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='regulation_competition', to='api.file'),
        ),
    ]