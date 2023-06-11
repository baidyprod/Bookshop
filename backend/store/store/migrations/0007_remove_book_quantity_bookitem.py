# Generated by Django 4.2.1 on 2023-06-10 20:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_book_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='quantity',
        ),
        migrations.CreateModel(
            name='BookItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('place', models.CharField(max_length=100)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
            ],
            options={
                'verbose_name': 'Book Item',
                'verbose_name_plural': 'Book Items',
            },
        ),
    ]