from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.core.exceptions import ObjectDoesNotExist
from .forms import MessageForm
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url='login/')
def mssg_all_page(request):
    user_to = User.objects.get(id = request.user.id)
    inbox = Message.objects.filter(reciver_deleted = False, mssg_to = user_to ).order_by('-delivery_date')
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
    return render(request,'mssg/mssg_page.html', {'inbox':inbox, 'current_mssg':current_mssg,})

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
    return render(request,'mssg/mssg_write.html')
