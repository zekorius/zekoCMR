import json
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils.html import linebreaks
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import MessageForm
from .models import Message
# Create your views here.
@login_required(login_url='login/')
def mssg_all_page(request):
    user_to = User.objects.get(id = request.user.id)
    inbox = Message.objects.filter(Q(reciver_deleted = False, mssg_to = user_to) | Q(deliver_deleted = False, mssg_from = user_to) ).order_by('-delivery_date')
    if request.method == "POST" and 'del-mssg' in request.POST:
        idtodel = request.POST.get('idtodel')
        mssgtodel = Message.objects.get(id = idtodel)
        if request.user == mssgtodel.mssg_from:
            mssgtodel.deliver_deleted = True
        if request.user == mssgtodel.mssg_to:
            mssgtodel.reciver_deleted = True
        if mssgtodel.deliver_deleted and mssgtodel.reciver_deleted:
            mssgtodel.delete()
        else:
            mssgtodel.save()
    elif request.method == "POST" and 'send-mssg' in request.POST:
        mssgform = MessageForm(request.POST)
        if mssgform.is_valid():
            newmssg = mssgform.save(commit = False)
            newmssg.mssg_to = User.objects.get(id = request.POST.get('mssg_to'))
            newmssg.mssg_from = User.objects.get(id = request.user.id)
            newmssg.save()
    #jquery & ajax
    elif request.method == "POST" and request.POST.get('option') == 'get_current':
        try:
            current_id = int(request.POST.get('c_id'))
            if Message.objects.get(id=current_id) in inbox:
                current_mssg = Message.objects.get(id=current_id)
            else:
                current_mssg = inbox.latest('delivery_date')
            print(current_mssg)
        except(ObjectDoesNotExist, ValueError):
            try:
                current_mssg = inbox.latest('delivery_date')
            except(ObjectDoesNotExist):
                current_mssg = False
        response_data = {}
        if current_mssg:
            response_data['id']=current_mssg.id
            response_data['title']=current_mssg.title
            response_data['text']=mark_safe(linebreaks(current_mssg.text))
            response_data['mssg_to']=current_mssg.mssg_to.username
            response_data['mssg_from']=current_mssg.mssg_from.username
            df = DateFormat(current_mssg.delivery_date)
            response_data['delivery_date']=df.format(get_format('DATE_FORMAT'))
            if current_mssg.mssg_to == request.user:
                current_mssg.been_read = True
                current_mssg.save()
            return JsonResponse(response_data )
        else:
            return JsonResponse({'no current message':'current message not found'})

    try:
        current_id = request.GET.get('current')
        if Message.objects.get(id=current_id) in inbox:
            current_mssg = Message.objects.get(id=current_id)
        else:
            current_mssg = inbox.latest('delivery_date')
    except(ObjectDoesNotExist, ValueError):
        try:
            current_mssg = inbox.latest('delivery_date')
        except(ObjectDoesNotExist):
            current_mssg = False
    if current_mssg and current_mssg.mssg_to == request.user:
        current_mssg.been_read = True
        current_mssg.save()

    #pagination
    if request.GET.get('page'):
        page = request.GET.get('page')
    else:
        page = 1
    paginator = Paginator(inbox, 5) # pokaż 5 na stronę
    try:
        inbox = paginator.page(page)
    except PageNotAnInteger:
        inbox = paginator.page(1) # jeżeli strona nie jest liczbą pokaż pierwszą
    except EmptyPage:
        inbox = paginator.page(paginator.num_pages) # jeżeli strona poza zasięgiem pokaż ostatnią

    mssgform = MessageForm()
    users = User.objects.all().order_by('username')
    return render(request,'mssg/mssg_page.html', {'inbox':inbox, 'current_mssg':current_mssg, 'users':users, 'mssgform':mssgform,})

@login_required(login_url='login/')
def mssg_to_page(request, user):
    if int(user) == 1488:
        print('1488!')
#        a = Message.objects.
    return render(request,'mssg/mmsg_page.html')

@login_required(login_url='login/')
def mssg_from_page(request, user):
    return render(request,'mssg/mmsg_page.html')

@login_required(login_url='login/')
def mssg_write(request):
    users = User.objects.all().order_by('username')
    if request.method == "POST" and 'send-mssg' in request.POST:
        mssgform = MessageForm(request.POST)
        if mssgform.is_valid():
            newmssg = mssgform.save(commit = False)
            newmssg.mssg_to = User.objects.get(id = request.POST.get('mssg_to'))
            newmssg.mssg_from = User.objects.get(id = request.user.id)
            newmssg.save()
    mssgform = MessageForm()
    return render(request,'mssg/mssg_write.html',{'users':users, 'mssgform':mssgform})
