# Generated by Django 2.2 on 2019-05-14 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_auto_20190513_1943'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subentry',
            options={'ordering': ['order', 'title'], 'verbose_name_plural': 'sub entries'},
        ),
        migrations.AddField(
            model_name='subentry',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
