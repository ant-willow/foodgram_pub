from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=100, verbose_name='Название', db_index=True)
    unit = models.CharField(max_length=50, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        # constraints = [models.UniqueConstraint(
        #     fields=['title', 'unit'], name='unique_ingredient')]

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор',
        related_name='recipes', on_delete=models.CASCADE)
    title = models.CharField(
        max_length=100, verbose_name='Название', db_index=True)
    image = models.ImageField(upload_to='recipes/', verbose_name='Картинка')
    description = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиенты', through='RecipeIngredient')
    breakfast_tag = models.BooleanField(verbose_name='завтрак', default=False)
    dinner_tag = models.BooleanField(verbose_name='обед', default=False)
    supper_tag = models.BooleanField(verbose_name='ужин', default=False)
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )
    prep_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент', on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'], name='unique_subscription')]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Избранное'
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favorite')]
