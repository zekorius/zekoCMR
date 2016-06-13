from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Companies
from .forms import AddCompany
from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.
@login_required(login_url='login/')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login/')
def companies_page(request):
    return render(request,'companies_page.html')

@login_required(login_url='login/')
def users_page(request):
    return render(request,'users_page.html')

@login_required(login_url='login/')
def strona_testowa(request):
    validError = False
    if request.method == "POST":
        formAdd = AddCompany(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('strona_testowa')
        else:
            companies = Companies.objects.all().order_by('name')
            validError = True
            return render(request, 'strona_testowa.html', {'companies': companies, 'formAdd': formAdd, 'validError': validError})
    else:
        formAdd = AddCompany()
        companies = Companies.objects.all().order_by('name')
    return render(request,'strona_testowa.html', {'companies': companies, 'formAdd': formAdd, 'validError': validError})
