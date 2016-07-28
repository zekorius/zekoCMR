from django.shortcuts import render
from .models import Categories
from .forms import CategoriesForm
from log.models import Companies
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def categories_page(request):
    default_del_try = False
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
            if(int(id_del) != 10): #in my project 10 is id of default category
                category_to_del = Categories.objects.get(id = id_del)
                companies = Companies.objects.filter(category = category_to_del)
                for company in companies:
                     company.category = Categories.objects.get(id = 10)
                     company.save()
                category_to_del.delete()
            else:
                print('Somebody tried to delete default category!')
                default_del_try = True
    categories = Categories.objects.all()
    form_category = CategoriesForm()
    return render(request,'categories_page.html',{'form_category':form_category,
                  'categories':categories, 'def_del':default_del_try,})
