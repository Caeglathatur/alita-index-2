# Generated by Django 2.2 on 2019-05-03 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(blank=True, default=None, help_text='CSS color.', max_length=50, null=True),
        ),
    ]