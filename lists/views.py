from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, render_to_response
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

# TODO:
#  NONE!

# Create your views here.


def home_page(request):
    return render(request=request, template_name='home.html', context={'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=list_)
            return redirect(to=list_)
    return render(request=request, template_name='list.html', context={'form': form, 'list': list_})


def new_list(request):
    """
    This view is for making new lists
    :param request: POST request with text payload
    :return: Redirect to view_list with the appropriate list id
    """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(to=list_)
    else:
        return render(request=request, template_name='home.html', context={'form': form})
