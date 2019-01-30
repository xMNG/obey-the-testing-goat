from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from functional_tests.base import FunctionalTest

User = get_user_model()

class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):
        """
        Helper function to create a logged in/auth session
        :param email: string email
        :return: None, creates pre-auth session in db
        """
        user = User.objects.create(email=email)
        session =  SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # to get a cookie, we visit a 404 url in the domain, since it loads fastest
        self.browser.get(url=self.live_server_url + "/404_no_such_url")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)

        # check to ensure logged out
        self.wait_to_be_logged_out(email=email)

        # edith is a logged in user and is redirected to the home page
        self.create_pre_authenticated_session(email=email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email=email)

        # she starts a list
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanetize eschaaton')
        first_list_url = self.browser.current_url

        # she notices a "My lists" link, for the first time and clicks it
        self.browser.find_element_by_link_text('My lists').click()

        # she sees her list items are there, and clicks on the first one
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Reticulate splines')
        )
        self.browser.find_element_by_link_text('Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(first=self.browser.current_url, second=first_list_url)
        )

        # she decides to start another list, just to see
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # under "my lists", her new list appears
        self.browser.find_element_by_link_text('My lists').click()
        self.wait_for(
            lambda: self.browser.find_element_by_link_text('Click cows').click()
        )
        self.browser.find_element_by_link_text('Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(first=self.browser.current_url, second=second_list_url)
        )

        # she logs out, The My Lists option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(
            first=self.browser.find_elements_by_link_text('My lists'), second=[]
        ))





