# Generated by Django 3.1.4 on 2021-01-14 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20210115_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Название'),
        ),
    ]
