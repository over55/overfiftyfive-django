# Generated by Django 2.0.13 on 2019-09-17 03:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0048_auto_20190906_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='police_check',
            field=models.DateField(blank=True, help_text='The date the staff took a police check.', null=True, verbose_name='Police Check'),
        ),
    ]
