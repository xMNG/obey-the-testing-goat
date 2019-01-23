from django.core import mail
from selenium.webdriver.common.keys import Keys
import re

from functional_tests.base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
    def test_can_get_email_link_to_log_in(self):
        # Edith goes to the awesome superlists site
        # and notices a "Log in" section int he navbar
        # It's telling her to enter her email address, so she does
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # A message appears telling her an email has been sent
        self.wait_for(lambda: self.assertIn(
            member='Check your email',
            container=self.browser.find_element_by_tag_name('body').text
        ))

        # she checks her email and finds a message:
        email = mail.outbox[0]
        self.assertIn(member=TEST_EMAIL, container=email.to)
        self.assertEqual(first=email.subject, second=SUBJECT)

        # It has a url link in it
        self.assertIn(member='Use this link to log in', container=email.body)
        url_search = re.search(pattern=r'http://.+/.+$', string=email.body)
        if not url_search:
            self.fail(msg=f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(member=self.live_server_url, container=url)

        # she clicks it
        self.browser.get(url)

        # she is logged in and sees a log out link
        self.wait_for(lambda: self.browser.find_element_by_link_text(link_text='Log out'))

        # checks for email in the navbar
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(member=TEST_EMAIL, container=navbar.text)
