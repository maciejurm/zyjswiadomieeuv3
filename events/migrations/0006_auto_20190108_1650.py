# Generated by Django 2.1.4 on 2019-01-08 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190108_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='localization',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Lokalizacja'),
        ),
    ]
