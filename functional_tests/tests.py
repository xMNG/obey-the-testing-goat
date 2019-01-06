import time
# import unittest

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"functional test checks for a user's story or experience to ensure it works"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"LiveServerTestCase is a live server but separate from sqlite3"



class NewVisitorTest(LiveServerTestCase):

    # TODO Does this setUp and tearDown in between every test function or the entire test?
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str):
        """
        Helper function for finding row text in table rows
        :param row_text: text to search for
        :return: None
        """
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'id_list_table')))
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # first user story
    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edit has heard about a cool new online to-do app. She goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types "Buy peacock features" into a text box (Edith's hobby is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists: "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.1)  # lets page refresh so explicit wait does not attach to element before redirect
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "use peacock feathers to make a fly" (Edith is very methodical"
        WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.ID, 'id_new_item')))
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(0.1)  # lets page refresh so explicit wait does not attach to element before redirect

        # The page updates again, and now shows both items on her list
        # Edith wonders whether the site will remember her list.
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')


        # Then she sees that the site has generated a unique URL for her -- there is some explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

        # self.fail('Finish the test!')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # she notices that her list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # now a new user, Francis, comes to the site
        # new session so nothing is saved
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # francis visits the home page. There is no sign of Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # francis starts a new list by entering a new item.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        # Edith goes to homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # She notices that the input box is centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        # She starts a new list and notices that the input is nicely centered there as well
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        # she sees that the new input box is still centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(first=inputbox.location['x'] + inputbox.size['width'] / 2, second=512, delta=10)

# removed because using django LiveTestCase runner to run these tests
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')



