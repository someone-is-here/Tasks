from datetime import datetime

from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login

from StationControlApp.forms import UserCreationForm, AddStationForm, AddIndicationForm
from StationControlApp.models import Station, Indication

from StationControlApp.serializers import StationSerializer, IndicationSerializer
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin,\
    DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions


class StationViewSet(CreateModelMixin,
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     DestroyModelMixin,
                     ListModelMixin,
                     GenericViewSet):
    """
    ViewSet associated with Station
    class which allows to create listview and create stations,
    update and delete them,
    also move station using Indication
    """
    queryset = Station.objects.all()
    serializer_class = StationSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), )

    @action(methods=['get', 'post'], detail=True, serializer_class=IndicationSerializer)
    def state(self, request, *args, **kwargs):
        """
        :param request: get
        :param args: -
        :param kwargs: pk of station
        :return: coords after changing

        :param request: post
        :param kwargs: pk of station
        get indication from user and move station
        :return: coords after changing
        """
        try:
            station = Station.objects.get(pk=kwargs['pk'])
        except:
            return Response({"error": "Object doesn't exists"})

        if request.method == 'POST':
            serializer = IndicationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            indication = Indication.objects.create(
                axis=request.data['axis'],
                distance=int(request.data['distance']),
                user=self.request.user,
            )
            indication.save()

            update_coords(station, indication)

        return Response({'x': station.x_position,
                         'y': station.y_position,
                         'z': station.z_position})


class StationsList(ListView):
    """
    class for displaying the view of all running stations
    """
    model = Station
    template_name = 'StationControlApp/index.html'
    context_object_name = 'stations'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'home'

        return context

    def get_queryset(self):
        return Station.objects.filter(state='running')


class ShowStation(DetailView):
    """
    class for showing all info about selected station
    """
    model = Station
    template_name = 'StationControlApp/station.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'


class ShowState(DetailView):
    """
    class for showing state about selected station
    state is positions (x,y,z)
    """
    model = Station
    template_name = 'StationControlApp/state.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'


def check_is_workable(distance, position, station):
    """

    :param distance: int. Distance we are moving
    :param position: int. Current position of selected axis
    :param station: type(Station). The station we are moving
    :return: int. Result position on axis
    """
    result_distance = position + distance

    if result_distance >= 0:
        station.state = station.STATES[0][1]
    else:
        station.state = station.STATES[1][1]
        station.time_broken = datetime.now()

    return result_distance


def update_coords(station, indication):
    """
    :param station: type(Station)
    :param indication: type(Indication)
    checks on which axis we are moving
    :return: None
    """
    if indication.axis == '1':
        distance = check_is_workable(indication.distance, station.x_position, station)
        station.x_position = distance
    elif indication.axis == '2':
        distance = check_is_workable(indication.distance, station.y_position, station)
        station.y_position = distance
    else:
        distance = check_is_workable(indication.distance, station.z_position, station)
        station.z_position = distance

    station.save()


class AddIndication(LoginRequiredMixin, CreateView):
    """
    class for creating indication
    """
    form_class = AddIndicationForm
    template_name = 'StationControlApp/create_indication.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'indication'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        indication = form.save()
        indication.user = self.request.user
        indication.save()
        station = Station.objects.get(pk=self.kwargs['station_id'])

        update_coords(station, indication)

        return redirect('station', self.kwargs['station_id'])


class AddStation(LoginRequiredMixin, CreateView):
    """
    class for adding station
    """
    form_class = AddStationForm
    template_name = 'StationControlApp/create_station.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        station = form.save()
        return redirect('station', station.id)


class UpdateStation(LoginRequiredMixin, UpdateView):
    """
    class for updating station
    """
    model = Station
    template_name = 'StationControlApp/update_station.html'
    fields = ['title', 'photo']
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'
    success_url = reverse_lazy('stations')
    login_url = reverse_lazy('login')


class DeleteStation(LoginRequiredMixin, DeleteView):
    """
    class for deleting station
    """
    model = Station
    pk_url_kwarg = 'station_id'
    template_name = 'StationControlApp/delete_station.html'
    context_object_name = 'station'
    success_url = reverse_lazy('stations')
    login_url = reverse_lazy('login')


class RegisterUser(CreateView):
    """
    class for register user
    after successful registration returns home(list with stations)
    """
    form_class = UserCreationForm
    template_name = 'StationControlApp/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('home')


class LoginUser(LoginView):
    from_class = AuthenticationForm
    template_name = 'StationControlApp/login.html'


def logout_user(request):
    logout(request)

    return redirect('login')
