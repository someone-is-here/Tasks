from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.exceptions import ErrorDetail

from StationControlApp.models import Station


class TestSetUp(APITestCase):
    client = APIClient()

    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'Help',
            'password1': '123',
            'password2': '123'
        }
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        # self.login_url = reverse('login')

        self.user_data_for_login = {
            'username': 'Help',
            'password': '123'
        }
        response = self.client.post(reverse('login'), data=self.user_data_for_login)
        self.assertEqual(response.status_code, 302)

        users = User.objects.all()
        self.assertEqual(users.count(), 1)

        self.client.post('/stations/', {'title': 'my_idea'}, format='json')
        self.client.logout()

        return super().setUp()

    def test_creating_station(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/', {'title': 'new idea'}, format='json')
        self.assertEqual(response.data['title'], 'new idea')
        self.assertEqual(response.status_code, 201)
        self.client.logout()

    def test_stations_get(self):
        response = self.client.get('/stations/')
        self.assertEqual(response.status_code, 200)

    def test_creating_station_error(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/', {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.client.logout()

    def test_stations_get_not_authenticated(self):
        self.client.post('/stations/', {'title': 'new idea'}, format='json')
        response = self.client.get('/stations/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    def test_station_get(self):
        response = self.client.get('/stations/1/')
        self.assertEqual(response.data['title'], 'my_idea')
        self.assertEqual(response.status_code, 200)

    def test_station_patch(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.patch('/stations/1/', {'title': 'new idea2'}, format='json')
        self.assertEqual(response.data['title'], 'new idea2')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_station_put(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.put('/stations/1/', {'title': 'new idea13'}, format='json')
        self.assertEqual(response.data['title'], 'new idea13')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_station_patch_no_authentication(self):
        response = self.client.patch('/stations/1/', {'title': 'new idea2'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_station_put_no_authentication(self):
        response = self.client.put('/stations/1/', {'title': 'new idea13'}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_station_delete(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.delete('/stations/1/')
        self.assertEqual(response.status_code, 204)
        self.client.logout()

    def test_station_delete_no_authentication(self):
        response = self.client.delete('/stations/1/')
        self.assertEqual(response.status_code, 403)

    def test_state_get_wrong(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.get('/stations/45/state/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': "Object doesn't exists"})
        self.client.logout()

    def test_state_get_exists_no_authentication(self):
        response = self.client.get('/stations/1/state/')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                               code='not_authenticated')})

    def test_state_get_exists_no_authentication(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.get('/stations/1/state/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"x": 100,
                                         "y": 100,
                                         "z": 100})
        self.client.logout()

    def test_state_post_doesnt_exists(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.get('/stations/45/state/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'error': "Object doesn't exists"})
        self.client.logout()

    def test_state_post_exists_axis_x(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 1, "distance": 23})
        self.assertEqual(response.data, {"x": 123,
                                         "y": 100,
                                         "z": 100})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_state_post_exists_axis_y(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 2, "distance": 23})
        self.assertEqual(response.data, {"x": 100,
                                         "y": 123,
                                         "z": 100})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_state_post_exists_axis_z(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 3, "distance": 23})
        self.assertEqual(response.data, {"x": 100,
                                         "y": 100,
                                         "z": 123})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_state_post_exists_axis_x_broken(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 1, "distance": -123})
        self.assertEqual(response.data, {"x": -23,
                                         "y": 100,
                                         "z": 100})
        station = Station.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(station.state, 'broken')
        self.client.logout()

    def test_state_post_exists_axis_y_broken(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 2, "distance": -123})
        self.assertEqual(response.data, {"x": 100,
                                         "y": -23,
                                         "z": 100})
        station = Station.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(station.state, 'broken')
        self.client.logout()

    def test_state_post_exists_axis_z_broken(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/1/state/', {"axis": 3, "distance": -123})
        self.assertEqual(response.data, {"x": 100,
                                         "y": 100,
                                         "z": -23})
        station = Station.objects.get(pk=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(station.state, 'broken')
        self.client.logout()

    def test_state_post_not_exists(self):
        self.client.post(reverse('login'), data=self.user_data_for_login)
        response = self.client.post('/stations/78/state/', {"axis": 3, "distance": -123})
        self.assertEqual(response.data, {'error': "Object doesn't exists"})
        self.assertEqual(response.status_code, 200)
        self.client.logout()
