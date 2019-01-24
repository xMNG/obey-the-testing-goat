from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import Token

User = get_user_model()  # TODO what does this do?

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

class TokenMethodTest(TestCase):

    def test_links_user_with_auto_generated_uid(self):
        token_1 = Token.objects.create(email='a@b.com')
        token_2 = Token.objects.create(email='a@b.com')
        self.assertNotEqual(first=token_1.uid, second=token_2.uid)