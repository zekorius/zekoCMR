from .models import Message
from django.contrib.auth.models import User

def inbox_processor(request):
    user = request.user
    inbox = Message.objects.filter(mssg_to = user).order_by('-delivery_date')[0:5]
    unread = Message.objects.filter(mssg_to = user).filter(been_read = False).count()
    return {'inbox_top': inbox, 'unread': unread}
