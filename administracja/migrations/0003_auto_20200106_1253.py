# Generated by Django 3.0.2 on 2020-01-06 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administracja', '0002_auto_20200106_1238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reader',
            old_name='description',
            new_name='desc',
        ),
    ]
