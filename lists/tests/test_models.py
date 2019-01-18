import os
import sys
from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Item, List

"Unit tests check for whether the code returns the correct result"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"No data is saved because django.test.TestCase doesn't touch the sqlite database"

sys.path.insert(0, os.path.abspath('..'))


class ItemModelTest(TestCase):
    """
    This tests the item model, not saving to the DB, does not use the app's sqlite3
    """

    def test_default_text(self):
        """
        Test that the default text is blank
        :return: Pass or fail
        """
        item = Item()
        self.assertEqual(
            first=item.text,
            second=''
        )

    def test_item_is_related_to_list(self):
        """
        Test that item associated with list appears in list's set.
        :return: Pass or fail
        """
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(member=item, container=list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        """
        Tests model to ensure validation on empty text is working
        :return: Pass or fail
        """
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_duplicate_items_are_invalid(self):
        """
        Tests to ensure validation error is raised when adding duplicate item to same list
        :return: Pass or fail
        """
        list_ = List.objects.create()
        Item.objects.create(list=list_, text='bla')

        with self.assertRaises(ValidationError):  # this is integrity error is constraint is enforced in the model
            item = Item(list=list_, text='bla')
            item.full_clean()  # this will catch blanks
            # item.save()  # this will catch unique_together but not blanks, raises integrity error

    def test_can_save_same_item_to_different_lists(self):
        """
        Tests that same item saved to different lists does not raise an error
        :return: Pass or fail
        """
        list_1 = List.objects.create()
        list_2 = List.objects.create()
        Item.objects.create(list=list_1, text='bla')
        item = Item(list=list_2, text='bla')
        item.full_clean()  # this should not raise an error

    def test_list_ordering(self):
        """
        Tests that list items are stored in order
        :return: Pass or fail
        """
        list_ = List.objects.create()
        item_1 = Item.objects.create(list=list_, text='item_1')
        item_2 = Item.objects.create(list=list_, text='item_2')
        item_3 = Item.objects.create(list=list_, text='item_3')

        self.assertEqual(
            first=list(Item.objects.all()),
            second=[item_1, item_2, item_3]
        )

    def test_string_representation(self):
        """
        Test that the string representation of the model objects are correct
        :return: Pass or fail
        """
        item = Item(text='some text')
        self.assertEqual(first=str(item), second='some text')


class ListModelTest(TestCase):
    """
    This tests the list model
    """
    def test_get_absolute_url(self):
        """
        Test to get the absolute URL from a list model object
        :return: Pass or fail
        """
        list_ = List.objects.create()
        self.assertEqual(first=list_.get_absolute_url(), second=f'/lists/{list_.id}/')
