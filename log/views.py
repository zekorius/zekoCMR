from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Companies
from .forms import CompanyForm

# Create your views here.
@login_required(login_url='login/')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login/')
def companies_page(request):
    validError = False
    if request.method == "POST" and request.POST.get('option')=='add':
        formAdd = CompanyForm(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            validError = True
            return render(request, 'companies_page.html', {'companies': companies, 'formAdd': formAdd, 'validError': validError})
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        companyToDel = Companies.objects.get(id=id_del)
        companyToDel.delete()
        return redirect('companies_page')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companyToEdit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companyToEdit.name = request.POST.get('name')
            companyToEdit.nip = request.POST.get('nip')
            companyToEdit.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            validError = True
            return render(request, 'companies_page.html', {'companies': companies, 'validError': validError})
    else:
        companies = Companies.objects.all().order_by('name')
    return render(request,'companies_page.html', {'companies': companies, 'validError': validError})

@login_required(login_url='login/')
def users_page(request):
    return render(request,'users_page.html')

@login_required(login_url='login/')
def strona_testowa(request):
    validError = False
    if request.method == "POST" and request.POST.get('option')=='add':
        formAdd = CompanyForm(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('strona_testowa')
        else:
            companies = Companies.objects.all().order_by('name')
            validError = True
            return render(request, 'strona_testowa.html', {'companies': companies, 'formAdd': formAdd, 'validError': validError})
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        companyToDel = Companies.objects.get(id=id_del)
        companyToDel.delete()
        return redirect('strona_testowa')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companyToEdit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companyToEdit.name = request.POST.get('name')
            companyToEdit.nip = request.POST.get('nip')
            companyToEdit.save()
            return redirect('strona_testowa')
        else:
            companies = Companies.objects.all().order_by('name')
            validError = True
            return render(request, 'strona_testowa.html', {'companies': companies, 'validError': validError})
    else:
        companies = Companies.objects.all().order_by('name')
    return render(request,'strona_testowa.html', {'companies': companies, 'validError': validError})


