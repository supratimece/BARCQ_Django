# Generated by Django 3.1.3 on 2020-12-16 14:27

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_auto_20201214_1946'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedcircuit',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='savedcircuit',
            name='circuit',
            field=jsonfield.fields.JSONField(null=True),
        ),
        migrations.DeleteModel(
            name='Circuit',
        ),
    ]