from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Companies, Comments
from .forms import CompanyForm, LookforForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# Create your views here.
@login_required(login_url='login/')
def home(request):
    return render(request,'home.html')

@login_required(login_url='login/')
def companies_page(request):
    page = request.GET.get('page')
    keyword = request.GET.get('search')
    sort_by = request.GET.get('order')
    sort_dic = {'cn':'name', '-cn':'-name', 'np':'nip', '-np':'-nip', 'ph':'phone','-ph':'-phone', 'ct':'city', '-ct':'-city', 'st':'st_address', '-st':'-st_address'}
    if not sort_by in sort_dic:
        sort_by = 'cn'
    been_searched = False
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
            if request.POST.get('name'):
                companytoedit.name = request.POST.get('name')
            if request.POST.get('phone'):
                companytoedit.phone = request.POST.get('phone')
            if request.POST.get('st_address'):
                companytoedit.address = request.POST.get('st_address')
            if request.POST.get('city'):
                companytoedit.city = request.POST.get('city')
            if request.POST.get('nip'):
                companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
            return redirect('companies_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error})
    elif keyword:
        companies = Companies.objects.all().order_by(sort_dic[sort_by]).filter(Q(nip__icontains = keyword)|Q(name__icontains = keyword))
        been_searched = True
    else:
        companies = Companies.objects.all().order_by(sort_dic[sort_by])

    paginator = Paginator(companies, 5) # pokaż 5 na stronę
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        companies = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią
    if been_searched and sort_by:
        return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error, 'search_phrase': keyword, 'sorted_by': sort_by })
    elif been_searched:
        return render(request, 'companies_page.html', {'companies': companies, 'valid_error': valid_error, 'search_phrase': keyword})
    elif sort_by:
        return render(request, 'companies_page.html', {'companies': companies, 'valid_error': valid_error, 'sorted_by': sort_by})
    return render(request,'companies_page.html', {'companies': companies, 'valid_error': valid_error, 'sort_by':'cn'})

@login_required(login_url='login/')
def users_page(request):
    page = request.GET.get('page')
    keyword = request.GET.get('search')
    been_searched = False
    password_not_match = False
    sort_by = request.GET.get('order')
    sort_dic = {'un':'username', '-un':'-username', 'e':'email', '-e':'-email',
    'fn':'first_name', '-fn':'-first_name', 'ln': 'last_name', '-ln': 'last_name'}
    if not sort_by in sort_dic:
        sort_by = 'un'
    users = User.objects.all().order_by('username')
    #post addition
    if request.method == "POST" and request.POST.get('option')=='add':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password!=password_re:
            password_not_match = True
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
    #post edition
    if request.method == "POST" and request.POST.get('option') == 'edit':
        nick = request.POST.get('nick')
        password = request.POST.get('password')
        password_re = request.POST.get('password_re')
        if password != password_re:
            password_not_match = True
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
    #post deletion
    elif request.method == "POST" and request.POST.get('option')=='del':
        id_del = request.POST.get('id_del')
        usertodel = User.objects.get(id=id_del)
        usertodel.delete()
        return redirect('users_page')
    elif keyword:
        users = User.objects.all().order_by(sort_dic[sort_by]).filter(Q(username__icontains = keyword)|Q(email__icontains = keyword)|Q(first_name__icontains = keyword)|Q(last_name__icontains = keyword))
        been_searched = True
    else:
        users = User.objects.all().order_by(sort_dic[sort_by])
    paginator = Paginator(users, 5) # pokaż 5 na stronę
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        users = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią
    if been_searched and sort_by:
        return render(request,'users_page.html', {'users': users, 'password_not_match': password_not_match, 'search_phrase': keyword, 'sorted_by': sort_by,})
    elif been_searched:
        return render(request,'users_page.html', {'users': users, 'password_not_match': password_not_match, 'search_phrase': keyword,})
    elif sort_by:
        return render(request,'users_page.html', {'users': users, 'password_not_match': password_not_match, 'sorted_by': sort_by,})
    return render(request,'users_page.html', {'users': users, 'password_not_match': password_not_match, 'sorted_by': 'un',})

@login_required(login_url='login/')
def company_details(request, id):
    comments = Comments.objects.filter(parent_id = id)
    print('jestem tutaj!')
    if request.POST.get('option') == 'add':
        print('a tutaj już nie :/')
        formAdd = CommentForm(request.POST)
        if formAdd.is_valid():
            new_comment = formAdd.save(commit=False)
            new_comment.parent_id = Companies.objects.get(id = id)
            new_comment.save()
            formAdd.save()


    try:
        company = Companies.objects.get(id = id)#id od firmy =id
    except ObjectDoesNotExist:
        return render(request, '404_company.html')
    except MultipleObjectsReturned:
        company = Companies.objects.filter(id = id).latest('id')
    return render(request,'company_details.html',{'comments': comments, 'company':company,})

@login_required(login_url='login/')
def test_page(request):
    page = request.GET.get('page')
    keyword = request.GET.get('search')
    sort_by = request.GET.get('order')
    sort_dic = {'cn':'name', '-cn':'-name', 'np':'nip', '-np':'-nip'}
    if not sort_by in sort_dic:
        sort_by = 'cn'
    been_searched = False
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
        return redirect('test_page')
    elif request.method == "POST" and request.POST.get('option')=='edit':
        id_edit = request.POST.get('id_edit')
        companytoedit = Companies.objects.get(id=id_edit)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            companytoedit.name = request.POST.get('name')
            companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
            return redirect('test_page')
        else:
            companies = Companies.objects.all().order_by('name')
            valid_error = True #    return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error})
    elif keyword:
        companies = Companies.objects.all().order_by(sort_dic[sort_by]).filter(Q(nip__icontains = keyword)|Q(name__icontains = keyword))
        been_searched = True
    else:
        companies = Companies.objects.all().order_by(sort_dic[sort_by])

    paginator = Paginator(companies, 5) # pokaż 5 na stronę
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        companies = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią
    if been_searched and sort_by:
        return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error, 'search_phrase': keyword, 'sorted_by': sort_by })
    elif been_searched:
        return render(request, 'test_page.html', {'companies': companies, 'valid_error': valid_error, 'search_phrase': keyword})
    elif sort_by:
        return render(request, 'test_page.html', {'companies': companies, 'valid_error': valid_error, 'sorted_by': sort_by})
    return render(request,'test_page.html', {'companies': companies, 'valid_error': valid_error, 'sort_by':'cn'})
