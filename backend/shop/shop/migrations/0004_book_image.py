# Generated by Django 4.2.1 on 2023-06-11 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_book_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
