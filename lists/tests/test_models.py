from django.test import TestCase
from ..models import Item, List
import os
import sys
sys.path.insert(0, os.path.abspath('..'))


"Unit tests check for whether the code returns the correct result"
"To run the functional tests: python manage.py test functional_tests"
"To run the unit tests: python manage.py test lists"
"To run both tests: python manage.py test"
"No data is saved because django.test.TestCase doesn't touch the sqlite database"


class ListAndItemModelTestCase(TestCase):
    """
    This tests the model, not saving to the DB, does not use the app's sqlite3
    """

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

