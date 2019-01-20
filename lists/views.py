from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, render_to_response
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm
# TODO:
#  NONE!

# Create your views here.


def home_page(request):
    return render(request=request, template_name='home.html', context={'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
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
        form.save(for_list=list_)
        return redirect(to=list_)
    else:
        return render(request=request, template_name='home.html', context={'form': form})
