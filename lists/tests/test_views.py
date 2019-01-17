import os
import sys

from django.test import TestCase
from django.utils.html import escape

from lists.models import Item, List
from lists.forms import ItemForm
from lists.forms import EMPTY_ITEM_ERROR

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

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def post_invalid_input(self):
        """
        Helper function to return invalid input as a response
        :return: HttpResponse obj for blank input
        """
        list_ = List.objects.create()
        return self.client.post(path=f'/lists/{list_.id}/', data={'text': ''})

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
                         data={'text': 'A new item for an existing list'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        _other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={'text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_item_form_in_list_view(self):
        """
        Test for form when viewing a list
        :return: Pass or Fail
        """
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(obj=response.context['form'], cls=ItemForm)
        self.assertContains(response=response, text='name="text"')

    def test_for_invalid_input_nothing_saved_to_db(self):
        """
        Test that no Item obj is in the db after attempting to enter invalid input
        :return: Pass or Fail
        """
        self.post_invalid_input()
        self.assertEqual(first=Item.objects.count(), second=0)

    def test_for_invalid_input_renders_list_template(self):
        """
        Test that the list.html template is rendered after an invalid input
        :return: Pass or Fail
        """
        response = self.post_invalid_input()
        self.assertEqual(first=response.status_code, second=200)
        self.assertTemplateUsed(response=response, template_name='list.html')

    def test_for_invalid_input_passes_form_to_template(self):
        """
        Test that the template has the form again after the invalid input
        :return: Pass or Fail
        """
        response = self.post_invalid_input()
        self.assertIsInstance(obj=response.context['form'], cls=ItemForm)

    def test_for_invalid_input_shows_error_on_page(self):
        """
        Test that the empty text form error appears on page
        :return: Pass or Fail
        """
        response = self.post_invalid_input()
        self.assertContains(response=response, text=escape(EMPTY_ITEM_ERROR))


class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        """
        This tests whether the data from POST is saved to the HTML (DB later)
        """
        # push this data to the post request
        self.client.post(path='/lists/new', data={'text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        """
        This tests for redirect after POST request
        """
        response = self.client.post(path='/lists/new', data={'text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response=response, expected_url=f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        """
        Tests for status code 200 and home.html after posting invalid blank input
        :return: Pass or Fail
        """
        response = self.client.post(path='/lists/new', data={'text': ''})
        self.assertEqual(first=response.status_code, second=200)
        self.assertTemplateUsed(response=response, template_name='home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        """
        Tests for empty item error on home page (redirect) after invalid input
        :return: Pass or Fail
        """
        response = self.client.post(path='/lists/new', data={'text': ''})
        # escape this or {% autoescape off %} @ template
        self.assertContains(response=response, text=escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        """
        Tests for form on home page after invalid input
        :return: Pass or Fail
        """
        response = self.client.post(path='/lists/new', data={'text': ''})
        # TODO look up how does this look up key in (OBEY chp 14)
        self.assertIsInstance(obj=response.context['form'], cls=ItemForm)

    def test_invalid_list_items_arent_saved(self):
        """
        Tests that no Item object is saved after invalid input
        :return: Pass or Fail
        """
        self.client.post(path='/lists/new', data={'text': ''})
        self.assertEqual(first=List.objects.count(), second=0)
