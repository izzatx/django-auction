# Generated by Django 4.1.7 on 2023-05-25 05:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='watchlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('watch_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.list')),
            ],
        ),
    ]