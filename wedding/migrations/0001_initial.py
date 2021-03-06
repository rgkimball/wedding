# Generated by Django 3.0.2 on 2020-03-24 00:41

from django.db import migrations, models
import django.db.models.deletion
import wedding.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('date', models.DateTimeField()),
                ('description', models.TextField()),
                ('location', models.TextField(default=None, null=True)),
                ('attire', models.TextField(default=None, null=True)),
                ('transportation', models.TextField(default=None, null=True)),
                ('parking', models.TextField(default=None, null=True)),
                ('other_info', models.TextField(default=None, null=True)),
                ('wedding_party_only', models.NullBooleanField(default=False)),
                ('rehearsal_only', models.NullBooleanField(default=False)),
                ('no_children', models.NullBooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('save_the_date_sent', models.DateTimeField(blank=True, default=None, null=True)),
                ('save_the_date_opened', models.DateTimeField(blank=True, default=None, null=True)),
                ('invitation_id', models.CharField(db_index=True, default=wedding.utils._random_uuid, max_length=32, unique=True)),
                ('invitation_sent', models.DateTimeField(blank=True, default=None, null=True)),
                ('invitation_opened', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_invited', models.BooleanField(default=False)),
                ('rehearsal_dinner', models.BooleanField(default=False)),
                ('wedding_party', models.BooleanField(default=False)),
                ('is_attending', models.NullBooleanField(default=None)),
                ('comments', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField()),
                ('last_name', models.TextField(blank=True, null=True)),
                ('email', models.TextField(blank=True, null=True)),
                ('is_attending', models.NullBooleanField(default=None)),
                ('meal', models.CharField(blank=True, choices=[('beef', 'Steak'), ('fish', 'Fish'), ('vegetarian', 'Vegetarian')], max_length=20, null=True)),
                ('is_child', models.BooleanField(default=False)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wedding.Party')),
            ],
        ),
    ]
