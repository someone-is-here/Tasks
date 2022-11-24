from django.urls import path
from django.contrib.auth import authenticate

from StationControlApp.views import stations, StationsList, ShowStation, RegisterUser, AddStation, LoginUser, \
    logout_user, DeleteStation, UpdateStation

urlpatterns = [
    path('', StationsList.as_view(), name='home'),
    path('home/', StationsList.as_view(), name='stations'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('stations/', StationsList.as_view(), name='stations'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('stations/<int:station_id>', ShowStation.as_view(), name='station'),
    path('stations/<int:station_id>/delete/', DeleteStation.as_view(), name='delete_station'),
    path('stations/<int:station_id>/update/', UpdateStation.as_view(), name='update_station'),
    path('stations/create', AddStation.as_view(), name='station'),
    path('stations/<int:station_id>/state/', stations),
]
# path('register/', RegisterUser.as_view(), name='register'),
# path('login/', login, name='login'),