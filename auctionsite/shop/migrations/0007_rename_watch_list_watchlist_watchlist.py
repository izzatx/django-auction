# Generated by Django 4.1.7 on 2023-05-30 20:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_remove_watchlist_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='watch_list',
            new_name='watchlist',
        ),
    ]
