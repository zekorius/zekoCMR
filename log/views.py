from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    password_match = False
    users = User.objects.all().order_by('username')
    #post addition
    if request.method == "POST" and request.POST.get('option')=='add':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password==password_re:
            password_match = True
        if password_match:
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
            return render(request,'users_page.html', {'users': users, 'password_match': password_match})
    #post edition
    if request.method == "POST" and request.POST.get('option') == 'edit':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password == password_re:
            password_match = True
        if password_match:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            id_edit = request.POST.get('id_edit')
            userToEdit = User.objects.get(id=id_edit)
            if nick:
                userToEdit.username = nick
            if password:
                userToEdit.set_password(password)
            if email:
                userToEdit.email = email
            if first_name:
                userToEdit.first_name = first_name
            if last_name:
                userToEdit.last_name = last_name
            userToEdit.save()
            return redirect('users_page')
        else:
            return render(request, 'users_page.html', {'users': users, 'password_match': password_match})
    #post deletion
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        userToDel = User.objects.get(id=id_del)
        userToDel.delete()
        return redirect('users_page')
    else:
        return render(request,'users_page.html', {'users': users})

@login_required(login_url='login/')
def strona_testowa(request):
    password_match = False
    users = User.objects.all().order_by('username')
    if request.method == "POST" and request.POST.get('option')=='add':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password==password_re:
            password_match = True
        if password_match:
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
            return redirect('strona_testowa')
        else:
            return render(request,'strona_testowa.html', {'users': users, 'password_match': password_match})
    #edycja posta
    if request.method == "POST" and request.POST.get('option') == 'edit':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password == password_re:
            password_match = True
        if password_match:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            id_edit = request.POST.get('id_edit')
            userToEdit = User.objects.get(id=id_edit)
            if nick:
                userToEdit.username = nick
            if password:
                userToEdit.set_password(password)
            if email:
                userToEdit.email = email
            if first_name:
                userToEdit.first_name = first_name
            if last_name:
                userToEdit.last_name = last_name
            userToEdit.save()
            return redirect('strona_testowa')
        else:
            return render(request, 'strona_testowa.html', {'users': users, 'password_match': password_match})
    #usuwanie
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        userToDel = User.objects.get(id=id_del)
        userToDel.delete()
        return redirect('strona_testowa')
    else:
        return render(request,'strona_testowa.html', {'users': users})

