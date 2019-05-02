# Generated by Django 2.2 on 2019-05-02 20:59

from django.db import migrations, models
import django.db.models.deletion
import index.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('discriminator', models.CharField(blank=True, help_text='Used for distinguishing two people with the same name. Human-readable and visible to users.', max_length=255)),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('slug', models.SlugField(unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='index.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Supports Markdown.')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('length', models.PositiveIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_visible', models.BooleanField(default=False)),
                ('authors', models.ManyToManyField(blank=True, related_name='entries', to='index.Author')),
                ('categories', models.ManyToManyField(blank=True, related_name='entries', to='index.Category')),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['title'],
            },
            bases=(index.models.BaseEntry, models.Model),
        ),
        migrations.CreateModel(
            name='IdentifierType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LengthUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Singular.', max_length=150)),
                ('name_plural', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SubEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, help_text='Supports Markdown.')),
                ('url', models.URLField(blank=True, verbose_name='URL')),
                ('length', models.PositiveIntegerField(blank=True, null=True)),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='index.Entry')),
            ],
            options={
                'verbose_name_plural': 'sub entries',
                'ordering': ['title'],
            },
            bases=(index.models.BaseEntry, models.Model),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='SubEntryIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('sub_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.SubEntry')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.IdentifierType')),
            ],
            options={
                'verbose_name_plural': 'sub entry identifiers',
            },
        ),
        migrations.AddField(
            model_name='subentry',
            name='identifier_types',
            field=models.ManyToManyField(blank=True, related_name='sub_entries', through='index.SubEntryIdentifier', to='index.IdentifierType'),
        ),
        migrations.AddField(
            model_name='subentry',
            name='length_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_entries', to='index.LengthUnit'),
        ),
        migrations.AddField(
            model_name='subentry',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='index.SubEntry'),
        ),
        migrations.CreateModel(
            name='EntryIdentifier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.Entry')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='index.IdentifierType')),
            ],
            options={
                'verbose_name_plural': 'entry identifiers',
            },
        ),
        migrations.AddField(
            model_name='entry',
            name='identifier_types',
            field=models.ManyToManyField(blank=True, related_name='entries', through='index.EntryIdentifier', to='index.IdentifierType'),
        ),
        migrations.AddField(
            model_name='entry',
            name='length_unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='entries', to='index.LengthUnit'),
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='entries', to='index.Tag'),
        ),
        migrations.AddConstraint(
            model_name='author',
            constraint=models.UniqueConstraint(fields=('name', 'discriminator'), name='unique_person'),
        ),
    ]
