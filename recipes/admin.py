from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, User


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    list_filter = (
        'title', 'author', 'breakfast_tag', 'dinner_tag', 'supper_tag')
    inlines = (RecipeIngredientInline,)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'unit')
    list_filter = ('title',)


class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
