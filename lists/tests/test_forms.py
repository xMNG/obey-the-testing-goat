from django.test import TestCase
from lists.forms import ItemForm

class ItemFormTestCase(TestCase):

    def test_form_renders_item_text_input(self):
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
            form.errors['text'],
            ["You can't have an empty list item"]
        )