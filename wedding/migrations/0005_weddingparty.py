# Generated by Django 3.0.2 on 2020-04-07 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0004_party_email_verfied'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeddingParty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('title', models.CharField(choices=[('MH', 'Maid of Honor'), ('BM', 'Best Man'), ('G', 'Groomsman'), ('B', 'Bridesmaid'), ('FG', 'Flower Girl'), ('RB', 'Ring Bearer')], default='B', max_length=2)),
                ('photo', models.URLField()),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
