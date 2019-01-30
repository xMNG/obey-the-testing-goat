import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

"functional test checks for a user's story or experience to ensure it works"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"[Static]LiveServerTestCase is a live server but separate from sqlite3"

"How to test: enter this in bash cmd line: "
"STAGING_SERVER=mng2.pythonanywhere.com python manage.py test functional_tests --failfast"

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait(function):
        """
        Decorator to wrap wait functions and isolate time features to this function
        :return: wrapped function in wait
        """
        def modified_function(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return function(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_function

    def add_list_item(self, list_item):
        """
        Adds list item to list and checks that item appears in list
        :param list_item: string to-do list item to add
        :return: None
        """
        num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
        self.get_item_input_box().send_keys(list_item)
        self.get_item_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {list_item}')


    @wait
    def wait_for_row_in_list_table(self, row_text: str):
        """
        Helper function for finding row text in table rows
        :param row_text: text to search for
        :return: None
        """
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, function_name):
        """
        Wait that pings the function periodically until timeout
        :param function_name: name of function, can be a lambda
        :return: function_name() result, or raises error
        """
        return function_name()

    def get_item_input_box(self):
        """
        Helper function to pick out input text box
        :return: Input text box browser node
        """
        time.sleep(1)
        return self.wait_for(lambda :self.browser.find_element_by_id('id_text'))

    @wait
    def wait_to_be_logged_in(self, email):
        self.browser.find_element_by_link_text('Log out')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertIn(member=email, container=navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        self.browser.find_element_by_name('email')
        navbar = self.browser.find_element_by_css_selector('.navbar')
        self.assertNotIn(member=email, container=navbar.text)



# removed because using django LiveTestCase runner to run these tests
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
