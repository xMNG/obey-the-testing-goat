from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

User = get_user_model()


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
        list_ = List()
        if request.user.is_authenticated:
            list_.owner = request.user
        list_.save()
        form.save(for_list=list_)
        return redirect(to=list_)
    else:
        return render(request=request, template_name='home.html', context={'form': form})

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request=request, template_name='my_lists.html', context={'owner': owner})