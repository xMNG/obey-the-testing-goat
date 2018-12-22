from django.test import TestCase
from .models import Item
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


"Unit tests check for whether the code returns the correct result"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"No data is saved because django.test.TestCase doesn't touch the sqlite database"


class HomePageTestCase(TestCase):
    """
    Test case for testing that the home page is uses correct template
    """
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ItemModelTestCase(TestCase):
    """
    This tests the model, not saving to the DB, does not use the app's sqlite3
    """

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        # checking if the new URL is still using home.html
        # TODO this will change to a different html later
        self.assertTemplateUsed(response=response, template_name='list.html')

        # assertContains returns 404 if URL doesn't exist
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        """
        This tests whether the data from POST is saved to the HTML (DB later)
        """
        # push this data to the post request
        self.client.post(path='/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        This tests for redirect after POST request
        """
        response = self.client.post(path='/lists/new', data={'item_text': 'A new list item'})
        # response code 302 = url redirect
        self.assertRedirects(response=response, expected_url='/lists/the-only-list-in-the-world/')
