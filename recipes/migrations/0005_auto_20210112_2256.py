# Generated by Django 3.1.4 on 2021-01-12 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210107_2130'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Любимое'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'Ингредиент рецепта', 'verbose_name_plural': 'Ингредиенты рецепта'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписка'},
        ),
    ]
