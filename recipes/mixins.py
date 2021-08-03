from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Q
from foodgram import settings

from .models import Favorite


class PaginatorMixin:
    def set_paginator(self, recipes):
        paginator = Paginator(recipes, settings.PAGE_SIZE)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        return paginator, page


class AnnotateFavoriteMixin:
    def annotate_favorited(self, recipes_list):
        fav_exists = (Favorite.objects.filter(
            recipe=OuterRef('pk'),
            user=self.request.user.is_authenticated and self.request.user))
        return recipes_list.annotate(favorited=Exists(fav_exists))


class TagFilterMixin:
    def tag_filter(self, queryset):
        tags = {tag: True for tag in self.request.GET if tag.endswith('tag')}
        tag_filter = Q()
        for key, value in tags.items():
            tag_filter |= Q(**{key: value})
        return queryset.filter(tag_filter)
