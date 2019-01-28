from unittest.mock import patch, call

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()  # TODO check under the hood for this

class AuthenticateTest(TestCase):

    def test_returns_None_if_no_such_token(self):
        """
        Tests a non-existent token to see if the authenticate function returns None
        :return: Pass or fail
        """
        result = PasswordlessAuthenticationBackend().authenticate('no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        """
        Test authenticate function to return the new user if the token is valid
        and no existing user in DB
        :return: Pass or fail
        """
        email = 'edith@example.com'
        token = Token.objects.create(email=email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        new_user = User.objects.get(email=email)  # returns Entry.doesNotExist if none
        self.assertEqual(first=user, second=new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        """
        Test authenticate function to return existing user if token is valid
        and existing user in DB
        :return: Pass or fail
        """
        existing_user = User.objects.create(email='edith@example.com')
        token = Token.objects.create(email=existing_user.email)
        user = PasswordlessAuthenticationBackend().authenticate(token.uid)
        self.assertEqual(first=user, second=existing_user)


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        """
        Gets correct user for a given email
        :return: Pass or fail
        """
        User.objects.create(email='another@example.com')
        desired_user = User.objects.create(email='edith@example.com')
        found_user = PasswordlessAuthenticationBackend().get_user(email='edith@example.com')
        self.assertEqual(first=found_user, second=desired_user)

    def test_returns_None_if_no_user_with_that_email(self):
        """
        Gets None for user if no matching user for an email
        :return: Pass or fail
        """
        self.assertIsNone(PasswordlessAuthenticationBackend().get_user(email='edith@example.com'))

