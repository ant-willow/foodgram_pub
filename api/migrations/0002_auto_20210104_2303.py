# Generated by Django 3.1.4 on 2021-01-04 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='author',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]
