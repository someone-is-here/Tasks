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
from StationControlApp.models import Station


class StationsList(ListView):
    model = Station
    template_name = 'StationControlApp/index.html'
    context_object_name = 'stations'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'home'
        # menu in context
        return context

    def get_queryset(self):
        return Station.objects.filter(state='running')


class ShowStation(DetailView):
    model = Station
    template_name = 'StationControlApp/station.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'


class AddIndication(LoginRequiredMixin, CreateView):
    form_class = AddIndicationForm
    template_name = 'StationControlApp/create_indication.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'indication'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        indication = form.save()
        indication.user = self.request.user
        indication.save()
        return redirect('station', self.kwargs['station_id'])


class AddStation(LoginRequiredMixin, CreateView):
    form_class = AddStationForm
    template_name = 'StationControlApp/create_station.html'
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        station = form.save()
        return redirect('station', station.id)


class UpdateStation(LoginRequiredMixin, UpdateView):
    model = Station
    template_name = 'StationControlApp/update_station.html'
    fields = ['title', 'photo']
    pk_url_kwarg = 'station_id'
    context_object_name = 'station'
    success_url = reverse_lazy('stations')
    login_url = reverse_lazy('login')


class DeleteStation(LoginRequiredMixin, DeleteView):
    model = Station
    pk_url_kwarg = 'station_id'
    template_name = 'StationControlApp/delete_station.html'
    context_object_name = 'station'
    success_url = reverse_lazy('stations')
    login_url = reverse_lazy('login')


def stations(request, station_id):
    return HttpResponse(f"Page loaded, station: {station_id}!")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>OOops! Something went wrong</h1>")


class RegisterUser(CreateView):
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
