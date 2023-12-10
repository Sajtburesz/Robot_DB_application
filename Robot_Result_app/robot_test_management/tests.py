from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from teams.models import Team,TeamMembership
from users.models import User
import json
from datetime import datetime
from robot_test_management.models import TestRun,Attributes,Comment,TestRun, TestSuite,Keyword, TestCase as TestCaseModel
from django.utils.timezone import make_aware
from django.utils import timezone

class TestRunCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.client.force_authenticate(user=self.user)
        self.team = Team.objects.create(name='Test Team',owner=self.user)
        TeamMembership.objects.create(team=self.team, user=self.user)
        self.url = reverse('testrun_upload')  

    def test_create_test_run_success(self):
        with open('test_data/output_1.xml', 'rb') as file:
            data = {
                'output_file': file,
                'team': self.team.id,
                'attributes': json.dumps({}),
                'is_public': False
            }
            response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_test_run_unauthenticated(self):
        self.client.force_authenticate(user=None) 
        with open('test_data/output_2.xml', 'rb') as file:
            data = {
                'output_file': file,
                'team': self.team.id,
                'attributes': json.dumps({}),  
                'is_public': False
            }
            response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_test_run_invalid_data(self):
        data = {
            'output_file': '',
            'team': self.team.id,
            'attributes': json.dumps({})
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class TestRunListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='testuser', email='user1@example.com', password='password123')
        self.another_user = User.objects.create_user(username='otheruser', email='user2@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

        self.team = Team.objects.create(name='Test Team', owner=self.user)
        self.another_team = Team.objects.create(name='Another Team', owner=self.another_user)

        self.test_run = TestRun.objects.create(team=self.team, is_public=False,attributes={}, executed_at=timezone.now())
        self.public_test_run = TestRun.objects.create(team=self.another_team, is_public=True,attributes={}, executed_at=timezone.now())

        self.url = reverse('testrun-list', kwargs={'teamId': self.team.id})

    def test_list_test_runs_for_forign_team(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
    
    def test_list_test_runs_for_team(self):
        TeamMembership.objects.create(team=self.team, user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.test_run.id, [run['id'] for run in response.data['results']])

    def test_list_test_runs_unauthenticated(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_public_test_runs(self):
        public_url = reverse('testrun-list', kwargs={'teamId': 'public'})
        response = self.client.get(public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.public_test_run.id, [run['id'] for run in response.data['results']])

    def test_list_test_runs_for_non_member(self):
        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestRunRetreiveViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team_member = User.objects.create_user(username='team_member',email='user1@example.com', password='password123')
        self.non_team_member = User.objects.create_user(username='non_team_member',email='user2@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team', owner=self.team_member)
        TeamMembership.objects.create(team=self.team, user=self.team_member)
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=False)
        self.url = reverse('testrun-instance', args=[self.team.id, self.test_run.id])

    def test_retrieve_as_team_member(self):
        self.client.force_authenticate(user=self.team_member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.test_run.id)

    def test_retrieve_as_non_team_member(self):
        self.client.force_authenticate(user=self.non_team_member)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_nonexistent_test_run(self):
        self.client.force_authenticate(user=self.team_member)
        non_existent_url = reverse('testrun-instance', args=[self.team.id, 999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class TestRunRetreiveViewActionTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.owner = User.objects.create_user(username='owner',email='user1@example.com', password='password123')
        self.member = User.objects.create_user(username='member',email='user2@example.com', password='password123')
        self.admin = User.objects.create_user(username='admin',email='user3@example.com', password='password123', is_staff=True)

        self.team = Team.objects.create(name='Test Team', owner=self.owner)
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=False)
        TeamMembership.objects.create(team=self.team, user=self.member)
        TeamMembership.objects.create(team=self.team, user=self.admin)
        TeamMembership.objects.create(team=self.team, user=self.owner)

        self.url = reverse('testrun-instance', args=[self.team.id, self.test_run.id])

    def test_edit_is_public_as_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.url, {'is_public': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_run.refresh_from_db()
        self.assertTrue(self.test_run.is_public)

    def test_edit_is_public_as_member(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.patch(self.url, {'is_public': True})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.test_run.refresh_from_db()
        self.assertFalse(self.test_run.is_public)

    def test_delete_test_run_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TestRun.objects.filter(id=self.test_run.id).exists())

    def test_delete_test_run_as_non_admin(self):
        self.client.force_authenticate(user=self.member)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class TestRunRetreivePublicViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user',email='user1@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team',owner=self.user)
        self.public_test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=True)
        self.private_test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=False)
        self.public_url = reverse('testrun-instance-public', args=[self.public_test_run.id])
        self.private_url = reverse('testrun-instance-public', args=[self.private_test_run.id])

    def test_retrieve_public_test_run(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.public_test_run.id)

    def test_retrieve_non_public_test_run(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.private_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_nonexistent_public_test_run(self):
        self.client.force_authenticate(user=self.user)
        nonexistent_url = reverse('testrun-instance-public', args=[999])
        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AttributeViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin_user = User.objects.create_user(username='admin',email='user1@example.com', password='password123', is_staff=True)
        self.non_admin_user = User.objects.create_user(username='nonadmin',email='user2@example.com', password='password123')

        self.attribute = Attributes.objects.create(key_name='sample_key')

    def test_edit_attribute_as_non_admin(self):
        self.client.force_authenticate(user=self.non_admin_user)
        url = reverse('attribute-key-edit', args=[self.attribute.id])
        response = self.client.patch(url, {'key_name': 'another_updated_key'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_attributes(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('attribute-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.attribute.key_name, [attr['key_name'] for attr in response.data['results']])
        
class CommentViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.another_user = User.objects.create_user(username='anotheruser',email='user2@example.com', password='password123')
        self.admin_user = User.objects.create_user(username='adminuser',email='user3@example.com', password='password123', is_staff=True)


        self.client.force_authenticate(user=self.user)

        self.team = Team.objects.create(name='Test Team', owner=self.user)
        TeamMembership.objects.create(team=self.team, user=self.user)
        TeamMembership.objects.create(team=self.team, user=self.another_user)
        TeamMembership.objects.create(team=self.team, user=self.admin_user)

        self.test_run = TestRun.objects.create(team=self.team, attributes={})
        self.comment = Comment.objects.create(author=self.user, testrun=self.test_run, text="Original Comment")
        self.url_list_create = reverse('comment-list-create', args=[self.team.id, self.test_run.id])
        self.url_retrieve_update_delete = reverse('comment-detail', args=[self.team.id, self.test_run.id, self.comment.id])
    
    def test_create_comment(self):
        data = {'testrun':self.test_run.id,'text': 'New Comment'}
        response = self.client.post(self.url_list_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)  
    
    def test_list_comments(self):
        response = self.client.get(self.url_list_create)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1) 
    
    def test_edit_comment_as_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {'testrun':self.test_run.id,'text': 'Edited Comment'}
        response = self.client.patch(self.url_retrieve_update_delete, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.text, 'Edited Comment')

    def test_edit_comment_as_non_owner(self):
        self.client.force_authenticate(user=self.another_user)
        data = {'text': 'Should Not Edit'}
        response = self.client.patch(self.url_retrieve_update_delete, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.url_retrieve_update_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

class TopFailingTestCasesViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team', owner=self.user)
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=True)
        self.suite = TestSuite.objects.create(name='Test Suite', test_run=self.test_run)
        self.url = reverse('top-failing-tcs', args=["public"]) 
        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 2', status='PASS', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        self.client.force_authenticate(user=self.user)
    def test_top_failing_test_cases(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(response.data), 5)
        failing_cases = [case['name'] for case in response.data]
        self.assertIn('Test Case 1', failing_cases)

class TreemapDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team', owner=self.user)
        now = make_aware(datetime.now())
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=True,executed_at=timezone.now())
        self.suite = TestSuite.objects.create(name='Test Suite', test_run=self.test_run)

        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 2', status='PASS', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        self.client.force_authenticate(user=self.user)

    def test_treemap_data(self):
        url = reverse('treemap-data', args=["public"]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for suite in response.data:
            self.assertIn('suite_name', suite)
            self.assertIn('total_cases', suite)
            self.assertIn('failed_cases', suite)

class TimelineDataViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team', owner=self.user)
        
        now = make_aware(datetime.now())
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=True,executed_at=timezone.now())
        self.suite = TestSuite.objects.create(name='Test Suite', test_run=self.test_run)

        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 2', status='PASS', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        
        
        self.client.force_authenticate(user=self.user)

    def test_timeline_data(self):
        url = reverse('timeline-data', args=["public"]) 
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for test_case in response.data:
            self.assertIn('test_case_name', test_case)
            self.assertIn('fail_periods', test_case)

class TestCaseDurationHeatmapDataTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email='user1@example.com', password='password123')
        self.team = Team.objects.create(name='Test Team', owner=self.user)
        self.test_run = TestRun.objects.create(team=self.team, attributes={}, is_public=True)
        self.suite = TestSuite.objects.create(name='Test Suite', test_run=self.test_run)

        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 2', status='PASS', suite=self.suite)
        TestCaseModel.objects.create(name='Test Case 1', status='FAIL', suite=self.suite)
        self.client.force_authenticate(user=self.user)

    def test_duration_heatmap_data(self):
        url = reverse('testcase-duration-heatmap-data', args=["public"])  
        post_data = {
            'suite_name': 'Test Suite Name',
            'date':  timezone.now().strftime('%Y-%m') 
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for entry in response.data:
            self.assertIn('testcase_name', entry)
            self.assertIn('overall_average_duration', entry)
            self.assertIn('daily_averages', entry)

