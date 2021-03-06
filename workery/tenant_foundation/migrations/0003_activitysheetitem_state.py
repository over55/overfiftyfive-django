# Generated by Django 2.0.5 on 2018-06-29 02:41

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0002_auto_20180628_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitysheetitem',
            name='state',
            field=django_fsm.FSMField(blank=True, db_index=True, default='pending', help_text='The state of this activity sheet item for the job offer.', max_length=50, verbose_name='State'),
        ),
    ]
