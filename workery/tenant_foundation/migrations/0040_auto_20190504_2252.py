# Generated by Django 2.0.10 on 2019-05-04 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0039_auto_20190504_2248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='associate',
            old_name='how_hear_about_us',
            new_name='how_hear',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='how_hear_about_us',
            new_name='how_hear',
        ),
        migrations.RenameField(
            model_name='partner',
            old_name='how_hear_about_us',
            new_name='how_hear',
        ),
        migrations.RenameField(
            model_name='staff',
            old_name='how_hear_about_us',
            new_name='how_hear',
        ),
    ]
