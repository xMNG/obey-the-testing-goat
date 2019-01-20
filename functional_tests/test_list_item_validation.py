from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def get_error_element(self):
        """
        Finds the error message via .has-error class
        :return: Returns error msg node
        """
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # edith goes to the home page and accidentally tries to submit an empty item, hits enter on empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # home page refreshes, error message appears saying items cannot be blank
        self.wait_for(lambda: self.browser.find_element_by_css_selector(css_selector='#id_text:invalid'))

        # she tries again with text, and it works
        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(css_selector='#id_text:valid'))

        # she submits it successfully
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # she tries to submit another empty text
        self.get_item_input_box().send_keys(Keys.ENTER)

        # receives similar warning
        self.wait_for(lambda: self.browser.find_element_by_css_selector(css_selector='#id_text:invalid'))

        # she submits some text
        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(css_selector='#id_text:valid'))
        self.get_item_input_box().send_keys(Keys.ENTER)

        # she sees her items on the list
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

    def test_cannot_add_duplicate_item(self):
        # go to web page
        self.browser.get(self.live_server_url)

        # find the input box and enter in text
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # wait for page to reload and check text in row
        self.wait_for_row_in_list_table('1: Buy wellies')

        # find the input box and enter in the same text again
        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # page returns error
        self.wait_for(lambda : self.assertEqual(
            self.get_error_element().text,
            second="You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        """
        Test to see if error messages are cleared upon text input
        :return: Pass or fail
        """
        # get page and send one item, then wait for it to appear
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Banter too thick')

        # send same item again and wait for message
        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # start typing to clear error
        self.get_item_input_box().send_keys('a')

        # error no longer is there
        self.wait_for(lambda :self.assertFalse(
            self.get_error_element().is_displayed()
        ))

# removed because using django LiveTestCase runner to run these tests
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
