from django.contrib import admin
from django.urls import path, include

from apps.commons.urls import urls as commons_urls
from apps.erm_tags.urls import urls as erm_tags_urls
from apps.jsonb_tags.urls import urls as jsonb_tags_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('commons/', include(commons_urls)),
    path('erm/', include(erm_tags_urls)),
    path('jsonb/', include(jsonb_tags_urls)),
]
