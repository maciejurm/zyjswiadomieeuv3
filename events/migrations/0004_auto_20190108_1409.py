# Generated by Django 2.1.4 on 2019-01-08 13:09

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20190104_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='body',
            field=tinymce.models.HTMLField(verbose_name='Szczegóły wydarzenia'),
        ),
        migrations.AlterField(
            model_name='event',
            name='localization',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Lokalizacja'),
        ),
    ]
