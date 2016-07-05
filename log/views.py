from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Companies
from .forms import CompanyForm, LookforForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url='login/')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login/')
def companies_page(request):
    page = request.GET.get('page')


    valid_error = False
    if request.method == "POST" and request.POST.get('option')=='add':
        formAdd = CompanyForm(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error})
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        companytodel = Companies.objects.get(id=id_del)
        companytodel.delete()
        return redirect('companies_page')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companytoedit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companytoedit.name = request.POST.get('name')
            companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error})
    elif request.method == "POST" and request.POST.get('option')=='search':
        keyword = request.POST.get('keyword')
        companies = Companies.objects.all().order_by('name').filter(name__contains = keyword)
    else:
        companies = Companies.objects.all().order_by('name')
        
    paginator = Paginator(companies, 5) # pokaż 5 na stronę
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        companies = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią
    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error})
    
'''
@login_required(login_url='login/')
def companies_page(request):
    valid_error = False
    if request.method == "POST" and request.POST.get('option')=='add':
        formAdd = CompanyForm(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True
            return render(request, 'companies_page.html', {'companies': companies, 'formAdd': formAdd, 'valid_error': valid_error})
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        companytodel = Companies.objects.get(id=id_del)
        companytodel.delete()
        return redirect('companies_page')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companytoedit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companytoedit.name = request.POST.get('name')
            companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True
            return render(request, 'companies_page.html', {'companies': companies, 'valid_error': valid_error})
    else:
        companies = Companies.objects.all().order_by('name')
    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error})
'''

@login_required(login_url='login/')
def users_page(request):
    password_not_match = True
    users = User.objects.all().order_by('username')
    #post addition
    if request.method == "POST" and request.POST.get('option')=='add':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password==password_re:
            password_not_match = False
        if not password_not_match:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            user = User.objects.create_user(nick)
            user.set_password(password)
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()
            return redirect('users_page')
        else:
            return render(request,'users_page.html', {'users': users, 'password_not_match': password_not_match})
    #post edition
    if request.method == "POST" and request.POST.get('option') == 'edit':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password == password_re:
            password_not_match = False
        if not password_not_match:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            id_edit = request.POST.get('id_edit')
            usertoedit = User.objects.get(id=id_edit)
            if nick:
                usertoedit.username = nick
            if password:
                usertoedit.set_password(password)
            if email:
                usertoedit.email = email
            if first_name:
                usertoedit.first_name = first_name
            if last_name:
                usertoedit.last_name = last_name
            usertoedit.save()
            return redirect('users_page')
        else:
            return render(request, 'users_page.html', {'users': users, 'password_not_match': password_not_match})
    #post deletion
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        usertodel = User.objects.get(id=id_del)
        usertodel.delete()
        return redirect('users_page')
    else:
        return render(request,'users_page.html', {'users': users})

@login_required(login_url='login/')
def test_page(request):
	
	
    
    page = request.GET.get('page')


    valid_error = False
    if request.method == "POST" and request.POST.get('option')=='add':
        formAdd = CompanyForm(request.POST)
        if formAdd.is_valid() and len(str(request.POST.get('nip'))) == 9:
            formAdd.save()
            return redirect('test_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error})
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        companytodel = Companies.objects.get(id=id_del)
        companytodel.delete()
        return redirect('companies_page')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companytoedit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companytoedit.name = request.POST.get('name')
            companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error})
    elif request.method == "POST" and request.POST.get('option')=='search':
        keyword = request.POST.get('keyword')
        companies = Companies.objects.all().order_by('name').filter(name__contains = keyword)
        #formKeyword = LookforForm({'keyword': request.POST.get('keyword')})
        #if formKeyword.is_valid():
        #    keyword = formKeyword.get_keyword()
        #    companies = Companies.objects.all().order_by('name').filter(name__contains = keyword)
        #else:
        #    valid_error = True
        #return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error})
    else:
        companies = Companies.objects.all().order_by('name')
        
    paginator = Paginator(companies, 5) # pokaż 5 na stronę
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        companies = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią
    return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error})

@login_required(login_url='login/')
def t2(request):
    return render(request, 't2.html')
