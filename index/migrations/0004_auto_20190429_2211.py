# Generated by Django 2.2 on 2019-04-29 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_auto_20190429_2008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='identifiers',
            new_name='identifier_types',
        ),
        migrations.AlterField(
            model_name='identifiertype',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
