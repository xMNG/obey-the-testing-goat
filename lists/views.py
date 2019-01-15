from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from .models import Item, List


# Create your views here.
# TODO
#  Remove duplication of validation logic in views


def home_page(request):
    return render(request=request, template_name='home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error_msg = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list= list_)  # does not create item, only instantiate
            item.full_clean()
            item.save()
            return redirect(to=list_)  # uses get_absolute_url() automatically
        except ValidationError:
            error_msg = "You can't have an empty list item"

    return render(request=request, template_name='list.html', context={'list': list_, 'error': error_msg})


def new_list(request):
    """
    This view is for making new lists
    :param request: POST request with text payload
    :return: Redirect to view_list with the appropriate list id
    """
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)  # instantiate, then call full_clean before saving
    try:
        item.full_clean()  # produces ValidationError if input inappropriate
        item.save()
    except ValidationError:
        list_.delete()
        error_msg = "You can't have an empty list item"
        return render(request=request, template_name='home.html', context={"error": error_msg})
    return redirect(to=list_)


