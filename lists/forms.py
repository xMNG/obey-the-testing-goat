from django import forms
from .models import Item

# class ItemForm(forms.Form):
#     """
#     This class is the manual way of doing a form via form class
#     """
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-lg',
#         })
#     )

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



