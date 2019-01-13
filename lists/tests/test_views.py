from django.test import TestCase
from django.utils.html import escape
from ..models import Item, List
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


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        # assertContains returns 404 if URL doesn't exist
        # check that correct_list contains the correct items
        self.assertContains(response=response, text='itemey 1')
        self.assertContains(response=response, text='itemey 2')

        # check that correct_list.id does not contain other list
        self.assertNotContains(response=response, text='other list item 1')
        self.assertNotContains(response=response, text='other list item 2')

    def test_passes_correct_list_to_template(self):
        _other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        _other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(f'/lists/{correct_list.id}/',
                         data={'item_text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        _other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_validation_error_ends_up_on_lists_page(self):
        list_= List.objects.create()
        response = self.client.post(
            path=f'/lists/{list_.id}/',
            data={'item_text': ''}
        )
        self.assertEqual(first=response.status_code, second=200)
        self.assertTemplateUsed(response=response, template_name='list.html')
        expected_error_msg = escape("You can't have an empty list item")
        self.assertContains(response=response, text=expected_error_msg)


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
        new_list = List.objects.first()
        self.assertRedirects(response=response, expected_url=f'/lists/{new_list.id}/')

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post(path='/lists/new', data={'item_text': ''})
        self.assertEqual(first=response.status_code, second=200)
        self.assertTemplateUsed(response=response, template_name='home.html')
        expected_error = escape("You can't have an empty list item")  # escape this or {% autoescape off %} @ template
        self.assertContains(response=response, text=expected_error)

    def test_invalid_list_items_arent_saved(self):
        self.client.post(path='/lists/new', data={'item_text': ''})
        self.assertEqual(first=List.objects.count(), second=0)
        self.assertEqual(first=List.objects.count(), second=0)
