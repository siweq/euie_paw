# Generated by Django 3.0.2 on 2020-01-12 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracja', '0018_remove_card_valid_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='valid_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
