from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User
from teams.models import Team, TeamMembership
from django.contrib.auth.hashers import make_password,check_password


class UserListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-list')

        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        User.objects.create(username='user1', password=make_password('password1'), email='user1@example.com')
        User.objects.create(username='user2', password=make_password('password2'), email='user2@example.com')
        User.objects.create(username='user3', password=make_password('password3'), email='user3@example.com')

    def test_list_users(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)  

    def test_ordering_users(self):
        response = self.client.get(f'{self.url}?ordering=username')
        usernames = [user['username'] for user in response.data['results']]  
        self.assertEqual(usernames, sorted(usernames))

    def test_filtering_users(self):
        response = self.client.get(f'{self.url}?username=user1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all('user1' in user['username'] for user in response.data['results'])) 

    def test_invalid_filtering(self):
        response = self.client.get(f'{self.url}?username=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0) 
class UserRetrieveUpdateDestroyViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.test_user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.target_user = User.objects.create_user(username='targetuser', email='targetuser@example.com', password='password123')

        self.url = reverse('user-detail', args=[self.target_user.username])

        self.client.force_authenticate(user=self.test_user)

    def test_retrieve_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'targetuser')

    def test_update_not_own_profile(self):
        desc = 'description'
        response = self.client.patch(self.url, {'email': desc})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        self.url = reverse('user-detail', args=[self.test_user.username])
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_unauthorized_update(self):
        self.client.force_authenticate(user=None)  
        response = self.client.patch(self.url, {'email': 'unauth@example.com'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_delete(self):
        self.client.force_authenticate(user=None)  
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserTeamsListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username='testuser', 
            email='asdasd@example.com', 
            password='password123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser', 
            email='dasdas@example.com', 
            password='password123'
        )

        self.team1 = Team.objects.create(name='Team 1', owner=self.user)
        self.team2 = Team.objects.create(name='Team 2', owner=self.user)

        TeamMembership.objects.create(team=self.team1, user=self.user)
        TeamMembership.objects.create(team=self.team2, user=self.user) 

        self.url = reverse('user-teams-list', args=[self.user.username])
        self.client.force_authenticate(user=self.user)

    def test_get_user_teams(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.team1.name, [team['name'] for team in response.data['results']])  

    def test_get_user_teams_no_teams(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  

    def test_unauthenticated_access(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            email='testuser@example.com', 
            password='old_password123'
        )
        self.client.force_authenticate(user=self.user)
        self.url = reverse('change-password')

    def test_change_password_success(self):
        payload = {'old_password': 'old_password123', 'new_password': 'newStrongPass123'}
        response = self.client.post(self.url, payload)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(check_password('newStrongPass123', self.user.password))

    def test_change_password_wrong_old_password(self):
        payload = {'old_password': 'wrong_old_password', 'new_password': 'newStrongPass123'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(check_password('old_password123', self.user.password)) 

    def test_change_password_invalid_new_password(self):
        payload = {'old_password': 'old_password123', 'new_password': 'short'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.user.refresh_from_db()
        self.assertTrue(check_password('old_password123', self.user.password)) 