from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer

class ProjectAPITestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpassword'
        }, format='json')
        
        self.access_token = response.data['access']

        self.project = Project.objects.create(name="Test Project", description="Description", owner=self.user)
    
    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_project(self):
        self.authenticate()
        url = reverse('project-list')
        data = {'name': 'New Project', 'description': 'New Project Description', 'owner':self.user.id}
        
        response = self.client.post(url, data, format='json')


        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Project')
        self.assertEqual(response.data['description'], 'New Project Description')

    def test_list_projects(self):
        self.authenticate()
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1) 

    def test_retrieve_project(self):
        self.authenticate()
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.project.name)

    def test_update_project(self):
        self.authenticate()
        url = reverse('project-detail', args=[self.project.id])
        data = {'name': 'Updated Project', 'description': 'Updated Description','owner': self.user.id}
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Project')

    def test_delete_project(self):
        self.authenticate()
        url = reverse('project-detail', args=[self.project.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
