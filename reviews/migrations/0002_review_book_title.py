# Generated by Django 4.2.1 on 2023-11-08 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='book_title',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
