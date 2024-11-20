from django.urls import reverse

from django.test import TestCase

from museamApp.models import User


class LoginPageTest(TestCase):
    def test_login_page(self):
        response = self.client.get(reverse('loginPage'))
        self.assertEqual(response.status_code, 200)
    def test_login_with_valid_credentials(self):
        user = User.objects.create_user(name='testUser', login='testUser', email='testads@gmai.com', password='testPassword')

        response = self.client.post(reverse('loginPage'), {'username': 'testUser', 'password': 'testPassword'})
        self.assertRedirects(response, reverse('employeePage'))

