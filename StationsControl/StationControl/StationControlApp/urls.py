from django.urls import path, include
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from StationControlApp.views import StationsList, ShowStation, RegisterUser, AddStation, LoginUser, \
    logout_user, DeleteStation, UpdateStation, AddIndication, ShowState, StationViewSet


router = routers.SimpleRouter()
router.register('', StationViewSet)

urlpatterns = [
    path('', StationsList.as_view(), name='home'),
    #rest
    path('stations/', include(router.urls)),
    path('stations/auth/', include('rest_framework.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    #ui
    path('ui/home/', StationsList.as_view(), name='stations'),

    path('ui/register/', RegisterUser.as_view(), name='register'),
    path('ui/login/', LoginUser.as_view(), name='login'),
    path('ui/logout/', logout_user, name='logout'),

    path('ui/stations/', StationsList.as_view(), name='stations'),
    path('ui/stations/<int:station_id>', ShowStation.as_view(), name='station'),
    path('ui/stations/<int:station_id>/delete/', DeleteStation.as_view(), name='delete_station'),
    path('ui/stations/<int:station_id>/update/', UpdateStation.as_view(), name='update_station'),

    path('ui/stations/create', AddStation.as_view(), name='create_station'),
    path('ui/stations/<int:station_id>/state/', ShowState.as_view(), name='state'),
    path('ui/stations/<int:station_id>/state/create', AddIndication.as_view(), name='create_indication'),
]
