# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from interestsapp.models import InterestRecords

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = "testuser"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user.save()

    def test_user_login_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_user_login_failure(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpassword',
        })
        self.assertRedirects(response, reverse(''))

    def test_dashboard_access(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_dashboard.html')

    def test_user_registration_success(self):
        response = self.client.post(reverse('register_user'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertRedirects(response, reverse(''))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        response = self.client.post(reverse('register_user'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword',
        })
        self.assertRedirects(response, reverse('user_creation'))

    def test_user_registration_username_exists(self):
        response = self.client.post(reverse('register_user'), {
            'username': self.username,
            'password1': 'password123',
            'password2': 'password123',
        })
        self.assertRedirects(response, reverse('user_creation'))

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse(''))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_send_interest(self):
        self.client.login(username=self.username, password=self.password)
        other_user = User.objects.create_user(username='otheruser', password='password123')
        response = self.client.post(reverse('sendInterest'), {
            'user_id': other_user.id,
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(InterestRecords.objects.filter(sender_id=self.user, receiver_id=other_user).exists())

    def test_send_interest_already_exists(self):
        self.client.login(username=self.username, password=self.password)
        other_user = User.objects.create_user(username='otheruser', password='password123')
        InterestRecords.objects.create(sender_id=self.user, receiver_id=other_user, status='Pending')
        response = self.client.post(reverse('sendInterest'), {
            'user_id': other_user.id,
        })
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'Interest request already exists.', status_code=400)

    def test_send_response(self):
        self.client.login(username=self.username, password=self.password)
        other_user = User.objects.create_user(username='otheruser', password='password123')
        interest = InterestRecords.objects.create(sender_id=other_user, receiver_id=self.user, status='Pending')
        response = self.client.post(reverse('sendResponse'), {
            'interest_id': interest.interest_id,
            'interest_status': 'Accepted',
        })
        interest.refresh_from_db()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(interest.status, 'Accepted')

class InterestManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.client.login(username='user1', password='password')

    def test_send_interest(self):
        response = self.client.post(reverse('sendInterest'), {
            'user_id': self.user2.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(InterestRecords.objects.filter(sender_id=self.user1, receiver_id=self.user2, status='Pending').exists())

    def test_send_interest_already_exists(self):
        InterestRecords.objects.create(sender_id=self.user1, receiver_id=self.user2, status='Pending')
        response = self.client.post(reverse('sendInterest'), {
            'user_id': self.user2.id
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['detail'], 'Interest request already exists.')

    def test_send_response(self):
        interest = InterestRecords.objects.create(sender_id=self.user1, receiver_id=self.user2, status='Pending')
        self.client.login(username='user2', password='password')
        response = self.client.post(reverse('sendResponse'), {
            'interest_id': interest.interest_id,
            'interest_status': 'Accepted'
        })
        self.assertEqual(response.status_code, 201)
        interest.refresh_from_db()
        self.assertEqual(interest.status, 'Accepted')

    def test_send_response_invalid_interest(self):
        response = self.client.post(reverse('sendResponse'), {
            'interest_id': 9999,  # Assuming this ID doesn't exist
            'interest_status': 'Accepted'
        })
        self.assertEqual(response.status_code, 404)

