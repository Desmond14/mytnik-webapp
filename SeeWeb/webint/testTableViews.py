from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from webint import views
from django.test.client import Client

class ContainerViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username='jacob', email='jacob@test.com', password='top_secret')
        User.objects.create_user(username='user1', email='user1@test.com')
        User.objects.create_user(username='user2', email='user2@test.com')
        User.objects.create_user(username='user3', email='user3@test.com')

    def test_proper_template_was_used(self):
        request = self.factory.get('/webint/containers/')
        request.user = self.user
        self.assertTemplateUsed('containers.html')

    def test_users_were_retrieved(self):
        self.client.login(username='jacob', password='top_secret')
        response = self.client.get("/webint/containers/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['users']), 4)

    def test_redirect_when_not_logged_in(self):
        response = self.client.get("/webint/containers/")
        self.assertRedirects(response, '/webint/not_logged_in/?next=/webint/containers/', status_code=302, target_status_code=200)