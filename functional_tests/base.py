import os
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


"functional test checks for a user's story or experience to ensure it works"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"[Static]LiveServerTestCase is a live server but separate from sqlite3"

"How to test: enter this in bash cmd line: "
"STAGING_SERVER=mng2.pythonanywhere.com python manage.py test functional_tests --failfast"


MAX_WAIT = 10

class FunctionalTest(StaticLiveServerTestCase):

    # TODO Does this setUp and tearDown in between every test function or the entire test?
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str):
        """
        Helper function for finding row text in table rows
        :param row_text: text to search for
        :return: None
        """
        WebDriverWait(self.browser, MAX_WAIT).until(ec.presence_of_element_located((By.ID, 'id_list_table')))
        WebDriverWait(self.browser, MAX_WAIT).until(ec.presence_of_element_located((By.TAG_NAME, 'tr')))
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for(self, function_name):
        """
        Wait that pings the function periodically until timeout
        :param function_name: name of function, can be a lambda
        :return: function_name() result, or raises error
        """
        start_time = time.time()
        while True:
            try:
                return function_name()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


# removed because using django LiveTestCase runner to run these tests
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
