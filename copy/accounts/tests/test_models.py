from django.contrib import auth
from django.test import TestCase
from accounts.models import Token

User = auth.get_user_model()  # TODO check under the hood

class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        """
        Test that the email is a valid email
        :return: Pass or fail
        """
        user = User(email='a@b.com')
        user.full_clean()  # should not raise

    def test_user_email_is_pk(self):
        """
        Test that the email is used as the pk
        :return: Pass or fail
        """
        user = User(email='a@b.com')
        self.assertEqual(first=user.email, second=user.pk)

    def test_no_problem_with_auth_login(self):
        user = User.objects.create(email='edith@example.com')
        user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request=request, user=user)  # should not raise

class TokenMethodTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token_1 = Token.objects.create(email='a@b.com')
        token_2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(first=token_1.uid, second=token_2.uid)