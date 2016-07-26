from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login/')
def categories_page(request):
    return render(request,'categories_page.html')
