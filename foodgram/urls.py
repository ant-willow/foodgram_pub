from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import include, path

flat_patterns = [
    path('us/', views.flatpage, {'url': '/about-us/'}, name='about_us'),
    path('spec/', views.flatpage, {'url': '/spec/'}, name='about_spec'),
    path('author/', views.flatpage, {'url': '/author/'}, name='about_author'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('about/', include(flat_patterns)),
    path('', include('recipes.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error' # noqa
