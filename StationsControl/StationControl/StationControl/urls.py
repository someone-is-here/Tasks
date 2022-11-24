from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from StationControl import settings
from StationControlApp.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('StationControlApp.urls'))
]


handler404 = page_not_found


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
