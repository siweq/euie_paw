# Generated by Django 3.0.2 on 2020-01-12 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracja', '0019_auto_20200112_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='main_card_id',
            field=models.CharField(blank=True, max_length=48, null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='administracja.Person'),
        ),
    ]
