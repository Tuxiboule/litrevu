# Generated by Django 4.2.1 on 2023-11-08 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_review_book_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='book_desc',
            field=models.CharField(blank=True, max_length=8192),
        ),
        migrations.AddField(
            model_name='review',
            name='book_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
