from unittest.mock import patch, call

from django.test import TestCase

from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        """
        Test checks for redirect to homepage after submitting email to log in
        :return Pass or fail
        """
        response = self.client.post(path='/accounts/send_login_email', data={'email': 'a@b.com'})
        self.assertRedirects(response=response, expected_url='/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post(self, mock_send_mail):
        self.client.post(path='/accounts/send_login_email', data={'email': 'edith@example.com'})

        self.assertTrue(expr=mock_send_mail.called)
        mock_send_mail_args, mock_send_mail_kwargs = mock_send_mail.call_args

        self.assertEqual(first=mock_send_mail_kwargs['subject'], second='Your login link for Superlists')
        self.assertEqual(first=mock_send_mail_kwargs['from_email'], second='noreply@superlists')
        self.assertEqual(first=mock_send_mail_kwargs['recipient_list'], second=['edith@example.com'])

    def test_creates_token_associated_with_email(self):
        self.client.post(path='/accounts/send_login_email', data={'email': 'edith@example.com'})
        token = Token.objects.first()
        self.assertEqual(first=token.email, second='edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post(path='/accounts/send_login_email', data={'email': 'edith@example.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'

        mock_send_mail_args, mock_send_mail_kwargs = mock_send_mail.call_args

        self.assertIn(member=expected_url, container=mock_send_mail_kwargs['message'])

    def test_adds_success_message(self):
        response = self.client.post(path='/accounts/send_login_email', data={'email': 'edith@example.com'}, follow=True)

        message = list(response.context['messages'])[0]
        self.assertEqual(
            first=message.message,
            second="Check your email, we've sent you a link you can use to log in."
        )
        self.assertEqual(first=message.tags, second="success")


@patch('accounts.views.auth')
class LoginViewTest(TestCase):

    def test_redirects_to_home_page(self, mock_auth):
        response = self.client.get(path=r'/accounts/login?token=abcd123', follow=True)
        self.assertRedirects(response=response, expected_url='/')

    def test_calls_authenticate_with_uid_from_get_request(self, mock_auth):
        self.client.get('/accounts/login?token=abcd123')
        self.assertTrue(mock_auth.authenticate.called)
        self.assertEqual(
            first=mock_auth.authenticate.call_args,
            second=call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            first=mock_auth.login.call_args,
            second=call(request=response.wsgi_request, user=mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(first=mock_auth.login.called, second=False)
