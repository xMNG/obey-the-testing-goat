from django.shortcuts import redirect, render
from .models import Item, List


# Create your views here.
def home_page(request):
    # render the view
    return render(request=request, template_name='home.html')


def view_list(request):
    # if this is a POST request to save an object, POST and redirect
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    items = Item.objects.all()
    return render(request=request, template_name='list.html', context={'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(to='/lists/the-only-list-in-the-world/')
