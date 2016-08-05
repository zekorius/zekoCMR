from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

# Create your models here.
class Message(models.Model):
    title = models.CharField(max_length = 60)
    mssg_from = models.ForeignKey(User, related_name = 'message_from', null = True, on_delete = models.SET_NULL )
    mssg_to = models.ForeignKey(User, related_name = 'message_to', null = True, on_delete = models.SET_NULL )
    text = models.TextField()
    been_read = models.BooleanField( default = False )
    reciver_deleted = models.BooleanField( default = False )
    deliver_deleted = models.BooleanField( default = False )
    delivery_date = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return 'Wiadomość "{}" wysłana przez {}  {}'.format(self.title, self.mssg_from.username, DateFormat(self.delivery_date).format(get_format('DATE_FORMAT')) )
