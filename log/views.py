from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Companies


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
    companies = Companies.objects.all().order_by('name')
    return render(request,'strona_testowa.html', {'companies': companies})
