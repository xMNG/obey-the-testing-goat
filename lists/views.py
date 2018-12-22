from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Item


# Create your views here.
def home_page(request):
    # if this is a POST request to save an object, POST and redirect
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    # render the view
    items = Item.objects.all()
    return render(request=request, template_name='home.html', context={'items': items})


def view_list(request):
    # if this is a POST request to save an object, POST and redirect
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    items = Item.objects.all()
    return render(request=request, template_name='list.html', context={'items': items})
