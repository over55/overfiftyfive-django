# Generated by Django 2.0.13 on 2020-03-10 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenant_foundation', '0073_workorder_closing_reason_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='indexed_text',
            field=models.CharField(blank=True, db_index=True, help_text='The searchable content text used by the keyword searcher function.', max_length=2047, null=True, unique=True, verbose_name='Indexed Text'),
        ),
    ]
