from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from users.models import User
from teams.models import Team, TeamMembership

class CreateTeamViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='creator', email='creator@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.url = reverse('create-team')

    def test_create_team_success(self):
        payload = {'name': 'New Team'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Team.objects.filter(name='New Team').exists())

    def test_create_team_unauthenticated(self):
        self.client.force_authenticate(user=None) 
        payload = {'name': 'New Team'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_team_no_data(self):
        payload = {}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_team_duplicate_name(self):
        Team.objects.create(name='Existing Team', owner=self.user)
        payload = {'name': 'Existing Team'}
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AddTeamMembersViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner_user = User.objects.create_user(username='owner',email='user0@example.com', password='password123')
        self.admin_user = User.objects.create_user(username='admin',email='user1@example.com', password='password123', is_staff=True, is_superuser=True)
        self.maintainer_user = User.objects.create_user(username='maintainer', email='user2@example.com', password='password123')
        self.member_user = User.objects.create_user(username='member',email='user3@example.com', password='password123')
        self.new_member = User.objects.create_user(username='new_member', email='user4@example.com',password='password123')

        self.team = Team.objects.create(name='Test Team', owner=self.owner_user)

        TeamMembership.objects.create(team=self.team, user=self.admin_user)
        TeamMembership.objects.create(team=self.team, user=self.maintainer_user, is_maintainer=True)
        TeamMembership.objects.create(team=self.team, user=self.member_user)

        self.url = reverse('add-members', args=[self.team.id])
    def test_add_wrong_payload_as_owner_(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {'members': ['notExistingUser']}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_member_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {'members': [self.admin_user.username,self.member_user.username,self.maintainer_user.username,self.new_member.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TeamMembership.objects.filter(team=self.team, user=self.new_member).exists())

    def test_add_member_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer_user)
        payload = {'members': [self.admin_user.username,self.member_user.username,self.maintainer_user.username,self.new_member.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(TeamMembership.objects.filter(team=self.team, user=self.new_member).exists())

    def test_add_member_as_member(self):
        self.client.force_authenticate(user=self.member_user)
        payload = {'members': [self.admin_user.username,self.member_user.username,self.maintainer_user.username,self.new_member.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RemoveTeamMembersViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner_user = User.objects.create_user(username='owner',email='user0@example.com', password='password123')
        self.admin_user = User.objects.create_user(username='admin',email='user1@example.com', password='password123', is_staff=True, is_superuser=True)
        self.maintainer_user = User.objects.create_user(username='maintainer', email='user2@example.com', password='password123')
        self.member_user = User.objects.create_user(username='member',email='user3@example.com', password='password123')

        self.team = Team.objects.create(name='Test Team', owner=self.owner_user)

        TeamMembership.objects.create(team=self.team, user=self.admin_user)
        TeamMembership.objects.create(team=self.team, user=self.maintainer_user, is_maintainer=True)
        TeamMembership.objects.create(team=self.team, user=self.member_user)

        self.url = reverse('remove-members', args=[self.team.id])

    def test_remove_wrong_payload_as_owner_(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {'members': ['notExistingUser']}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_member_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        payload = {'members': [self.maintainer_user.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TeamMembership.objects.filter(team=self.team, user=self.maintainer_user).exists())

    def test_remove_member_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer_user)
        payload = {'members': [self.member_user.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(TeamMembership.objects.filter(team=self.team, user=self.member_user).exists())

    def test_remove_member_as_member(self):
        self.client.force_authenticate(user=self.member_user)
        payload = {'members': [self.maintainer_user.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_remove_admin_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer_user)
        payload = {'members': [self.admin_user.username]}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class RetrieveUpdateDestroyTeamViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(username='owner',email='user0@example.com', password='password123')
        self.admin = User.objects.create_user(username='admin',email='user1@example.com', password='password123', is_staff=True, is_superuser=True)
        self.maintainer = User.objects.create_user(username='maintainer', email='user2@example.com', password='password123')
        self.member = User.objects.create_user(username='member',email='user3@example.com', password='password123')

        self.team = Team.objects.create(name='Test Team', owner=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.member)
        TeamMembership.objects.create(team=self.team, user=self.maintainer, is_maintainer=True)
        TeamMembership.objects.create(team=self.team, user=self.admin)


        self.url = reverse('manage-team', args=[self.team.id])

    def test_retrieve_team(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')
        self.assertEqual(response.data['owner'], self.owner.username)

    def test_update_team_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        payload = {'name': 'Updated Team Name'}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.team.refresh_from_db()
        self.assertEqual(self.team.name, 'Updated Team Name')

    def test_update_team_as_member(self):
        self.client.force_authenticate(user=self.member)
        payload = {'name': 'Attempted Update by Member'}
        response = self.client.put(self.url, payload)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_team_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_team_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer)
        response = self.client.delete(self.url)
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class LeaveTeamViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(username='owner',email='user0@example.com', password='password123')
        self.admin = User.objects.create_user(username='admin',email='user1@example.com', password='password123', is_staff=True, is_superuser=True)
        self.maintainer = User.objects.create_user(username='maintainer', email='user2@example.com', password='password123')
        self.member = User.objects.create_user(username='member',email='user3@example.com', password='password123')
        self.member2 = User.objects.create_user(username='member2',email='user4@example.com', password='password123')

        self.team = Team.objects.create(name='Test Team', owner=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.member)
        TeamMembership.objects.create(team=self.team, user=self.maintainer, is_maintainer=True)
        TeamMembership.objects.create(team=self.team, user=self.admin)


        self.url = reverse('leave-team', args=[self.team.id])

    def test_leave_team_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_leave_team_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_leave_team_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_leave_team_as_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_leave_not_existing_team_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer)
        response = self.client.post(reverse('leave-team', args=[1000000]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_leave_wrong_team_as_member(self):
        self.client.force_authenticate(user=self.member2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateRoleViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(username='owner',email='user1@example.com',password='password123')
        self.admin = User.objects.create_user(username='admin',email='user2@example.com', password='password123', is_staff=True)
        self.maintainer = User.objects.create_user(username='maintainer',email='user3@example.com', password='password123')
        self.member = User.objects.create_user(username='member',email='user4@example.com',password='password123')

        self.team = Team.objects.create(name='Test Team', owner=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.owner)
        TeamMembership.objects.create(team=self.team, user=self.admin)
        TeamMembership.objects.create(team=self.team, user=self.maintainer, is_maintainer=True)
        TeamMembership.objects.create(team=self.team, user=self.member)

        self.url = reverse('roles', args=[self.team.id])

    def test_update_role_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        payload = {'username': self.member.username, 'new_role': 'maintainer'}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        payload = {'username': self.maintainer.username, 'new_role': 'member'}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_as_maintainer(self):
        self.client.force_authenticate(user=self.maintainer)
        payload = {'username': self.member.username, 'new_role': 'maintainer'}
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_role_as_member(self):
        self.client.force_authenticate(user=self.member)
        payload = {'username': self.maintainer.username, 'new_role': 'member'}
        response = self.client.put(self.url, payload)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
