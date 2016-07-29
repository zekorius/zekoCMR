from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Message(models.Model):
    title = models.CharField(max_length = 60)
    mssg_from = models.ForeignKey(User, related_name = 'message_from', null = True, on_delete = models.SET_NULL )
    mssg_to = models.ForeignKey(User, related_name = 'message_to', null = True, on_delete = models.SET_NULL )
    text = models.TextField()
    reciver_deleted = models.BooleanField( default = False )
    deliver_deleted = models.BooleanField( default = False )
    delivery_date = models.DateTimeField(auto_now = True, auto_now_add = False)

    def __str__(self):
        return 'Wiadomość "{}" wysłana przez {}  {}'.format(self.title, self.mssg_from.username, self.delivery_date)
