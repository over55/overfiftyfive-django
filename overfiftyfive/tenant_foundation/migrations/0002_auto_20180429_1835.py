# Generated by Django 2.0.4 on 2018-04-29 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='associate',
            name='is_contract_time',
        ),
        migrations.RemoveField(
            model_name='associate',
            name='is_full_time',
        ),
        migrations.RemoveField(
            model_name='associate',
            name='is_part_time',
        ),
    ]
