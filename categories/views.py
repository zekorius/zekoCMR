from django.shortcuts import render
from .models import Categories
from .forms import CategoriesForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def categories_page(request):
    if request.method == "POST":
        if 'add_category' in request.POST:
            form_category = CategoriesForm(request.POST)
            if form_category.is_valid():
                form_category.save()
        elif 'edit_category' in request.POST:
            id_edit = request.POST.get('id_edit')
            category_edited = Categories.objects.get(id = id_edit)
            category_edited.name = request.POST.get('name')
            category_edited.color = request.POST.get('color')
            category_edited.save()
        elif 'delete_category' in request.POST:
            id_del = request.POST.get('id_del')
            category_to_del = Categories.objects.get(id = id_del)
            category_to_del.delete()
    categories = Categories.objects.all()
    form_category = CategoriesForm()
    return render(request,'categories_page.html',{'form_category':form_category,
                                                  'categories':categories,})
