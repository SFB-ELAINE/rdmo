# Generated by Django 2.2.2 on 2019-06-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('domain', '0043_django2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='level',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='lft',
            field=models.PositiveIntegerField(editable=False),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='rght',
            field=models.PositiveIntegerField(editable=False),
        ),
    ]