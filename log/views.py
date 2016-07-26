from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from .models import Companies, Comments, PdfFiles
from .forms import CompanyForm, LookforForm, CommentForm, PdfFilesForm
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
    sort_dic = {'cn':'name', '-cn':'-name', 'np':'nip', '-np':'-nip',
    'ph':'phone','-ph':'-phone', 'ct':'city', '-ct':'-city', 'st':'st_address',
    '-st':'-st_address'}
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
        commentstodel = Comments.objects.filter(company = companytodel)
        commentstodel.delete()
        docstodel = PdfFiles.objects.filter(company = companytodel)
        docstodel.delete()
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
                companytoedit.st_address = request.POST.get('st_address')
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
        companies = Companies.objects.all().order_by(sort_dic[sort_by]).filter( Q(nip__icontains = keyword)|Q(name__icontains = keyword)|Q(city__icontains = keyword)|Q(phone__icontains = keyword)|Q(st_address__icontains = keyword) )
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
    comments = Comments.objects.filter(company = id)
    formComment = CommentForm()
    uploaded = False
    invalid_data = False
    if request.method == "POST" and 'add-comment' in request.POST:
        auth_id = (request.POST.get('id_user'))
        formComment = CommentForm(request.POST)
        if formComment.is_valid():
            new_comment = formComment.save(commit=False)
            new_comment.company = Companies.objects.get(id = id)
            new_comment.author = User.objects.get(id = auth_id)
            new_comment.save()
    if request.method == "POST" and 'edit-comment' in request.POST:
        formComment = CommentForm(request.POST)
        if formComment.is_valid():
            id_edit = request.POST.get('id_edit')
            comment_to_edit = Comments.objects.get(id=id_edit)
            if request.POST.get('title'):
                comment_to_edit.title = request.POST.get('title')
            if request.POST.get('text'):
                comment_to_edit.text = request.POST.get('text')
            comment_to_edit.save()
    elif request.method == "POST" and request.POST.get('option') == 'edit':
        companytoedit = Companies.objects.get(id=id)
        formEdit = CompanyForm(request.POST)
        if formEdit.is_valid() and len(str(request.POST.get('nip'))) == 9:
            if request.POST.get('name'):
                companytoedit.name = request.POST.get('name')
            if request.POST.get('phone'):
                companytoedit.phone = request.POST.get('phone')
            if request.POST.get('st_address'):
                companytoedit.st_address = request.POST.get('st_address')
            if request.POST.get('city'):
                companytoedit.city = request.POST.get('city')
            if request.POST.get('nip'):
                companytoedit.nip = request.POST.get('nip')
            companytoedit.save()
        else:
            valid_error = True
    elif request.method == "POST" and request.POST.get('option') == 'del':
        id_del = id
        companytodel = Companies.objects.get(id = id_del)
        commentstodel = Comments.objects.filter(company = companytodel)
        commentstodel.delete()
        docstodel = PdfFiles.objects.filter(company = companytodel)
        docstodel.delete()
        companytodel.delete()
        return redirect('companies_page')
    elif request.method == "POST" and request.POST.get('option') == 'dl-cmt':
        id_del = request.POST.get('id_del')
        commenttodel = Comments.objects.get(id = id_del)
        commenttodel.delete()
        #return redirect('company_details', id = id)
    elif request.method == "POST" and request.POST.get('option') == 'add_pdf':
        pdf_form = PdfFilesForm(request.POST, request.FILES)
        try:
            if pdf_form.is_valid():
                newfile = PdfFiles(companypdf = request.FILES['companypdf'],
                company =  Companies.objects.get(id = id))
                uploaded = ((newfile.companypdf.size < 104857600) and (newfile.companypdf.name.endswith('.pdf')) )
                if not uploaded:
                    raise
                else:
                    newfile.save()
        except:
            invalid_data = True
    elif request.method == "POST" and request.POST.get('option') == 'del_pdf':
        id_del = request.POST.get('id_del')
        doctodel = PdfFiles.objects.get(id = id_del)
        doctodel.delete()
    try:
        company = Companies.objects.get(id = id)#id od firmy =id
    except ObjectDoesNotExist:
        return render(request, '404_company.html')
    except MultipleObjectsReturned:
        company = Companies.objects.filter(id = id).latest('id')
    pdf_form = PdfFilesForm()
    pdf_files = PdfFiles.objects.filter(company = company)
    return render(request,'company_details.html',{'comments': comments,
                  'company':company, 'comment_form':formComment,
                  'pdf_files':pdf_files, 'uploaded':uploaded,
                  'invalid_data':invalid_data, 'pdf_form':pdf_form})

@login_required(login_url='login/')
def test_page(request):
    print('niby jestem w test_page')
    uploaded = False
    invalid_data = False
    if request.method == "POST" and request.POST.get('option')=='add_pdf':
        pdf_form = PdfFilesForm(request.POST, request.FILES)
        print(Companies.objects.get(id = 1))
        try:
            if pdf_form.is_valid():
                newfile = PdfFiles(companypdf = request.FILES['companypdf'],
                                   company =  Companies.objects.get(id = 1))
                # print('forma działa\n a plik to:')
                # print(newfile.companypdf)
                # print('teraz przydałoby się sprawdzić czy jest pdfem')
                # print(newfile.companypdf.name.endswith('.pdf'))
                # print('teraz przydałoby się sprawdzić czy jest <100Mb')
                # print(newfile.companypdf.size)
                # print(newfile.companypdf.size < 104857600)
                uploaded = ((newfile.companypdf.size < 104857600) and (newfile.companypdf.name.endswith('.pdf')) )
                if not uploaded:
                    raise
                else:
                    newfile.save()
        except:
            invalid_data = True
    elif request.method == "POST" and request.POST.get('option')=='del_pdf':
        id_del = request.POST.get('id_del')
        doctodel = PdfFiles.objects.get(id = id_del)
        doctodel.delete()
    pdf_form = PdfFilesForm()
    pdf_files = PdfFiles.objects.all()
    return render(request,'test_page.html',{'pdf_form':pdf_form, 'pdf_files':pdf_files,'uploaded':uploaded, 'invalid_data':invalid_data,})
