from django import forms
from .models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


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




