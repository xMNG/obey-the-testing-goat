from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        """
        Tests CSS layout and styling
        :return: None
        """
        # Edith goes to homepage
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        # She notices that the input box is centered
        inputbox = self.get_item_input_box()
        # She starts a new list and notices that the input is nicely centered there as well
        self.add_list_item('testing')
        # inputbox.send_keys('testing')
        # inputbox.send_keys(Keys.ENTER)
        # she sees that the new input box is still centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(first=inputbox.location['x'] + inputbox.size['width'] / 2, second=512, delta=10)


# removed because using django LiveTestCase runner to run these tests
# if __name__ == '__main__':
#     unittest.main(warnings='ignore')
