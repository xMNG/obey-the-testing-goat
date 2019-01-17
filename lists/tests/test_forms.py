from django.test import TestCase
from lists.forms import ItemForm
from lists.models import Item
from lists.models import List

class ItemFormTestCase(TestCase):

    def test_form_renders_text_input(self):
        """
        Check if the form renders the placeholders and class
        :return: Pass or Fail
        """
        form = ItemForm()
        self.assertIn(member='placeholder="Enter a to-do item"', container=form.as_p())
        self.assertIn(member='class="form-control input-lg"', container=form.as_p())

    def test_form_validation_for_blank_items(self):
        """
        Check if the form validates for blank items
        :return: Pass or fail
        """
        # send blank line to text input of form
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            first=form.errors['text'],
            second=["You can't have an empty list item"]
        )

    def test_form_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'fake text'})
        new_item = form.save(for_list=list_)
        self.assertEqual(first=new_item, second=Item.objects.first())
        self.assertEqual(first=new_item.text, second='fake text')
        self.assertEqual(first=new_item.list, second=list_)