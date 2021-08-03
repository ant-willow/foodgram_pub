
from django import template

register = template.Library()


@register.filter
def is_favorited(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def is_subscribed(author, user):
    return user.subscriptions.filter(author=author).exists()
