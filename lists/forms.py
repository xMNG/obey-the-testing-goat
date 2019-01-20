from django import forms
from django.core.exceptions import ValidationError

from .models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this in your list"

class ItemForm(forms.models.ModelForm):
    """
    This is the form that is based on a model
    """

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter a to-do item',
            'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR},
        }

    def save(self, for_list):
        """
        Overrides save to include a list
        :param for_list: list object from lists.models
        :return: Saves object to DB
        """
        self.instance.list = for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    # TODO learn this!!
    def __init__(self, for_list, *args, **kwargs):
        """
        Uses parent constructor
        :param for_list: List obj
        :param args: str text data
        :param kwargs: Other
        """
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    # TODO learn this!!
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}  # adds custom error message
            self._update_errors(e)  # updates error

    def save(self):
        return forms.models.ModelForm.save(self)



