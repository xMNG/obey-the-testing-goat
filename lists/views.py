from django.shortcuts import redirect, render
from .models import Item, List


# Create your views here.
def home_page(request):
    # render the view
    return render(request=request, template_name='home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request=request, template_name='list.html', context={'list': list_})


def new_list(request):
    """
    This view is for making new lists
    :param request: POST request with text payload
    :return: Redirect to view_list with the appropriate list id
    """
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(to=f'/lists/{list_.id}/')


def add_item(request, list_id):
    """
    This view is for adding to an existing list
    :param request: POST request with text payload
    :param list_id: list id given via URL regex group
    :return: Redirect to view_list with the appropriate list id
    """
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
