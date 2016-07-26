from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Companies(models.Model):
    name = models.CharField(max_length = 70)
    nip = models.IntegerField()
    st_address = models.CharField(max_length = 40)
    city = models.CharField(max_length = 30)
    phone = models.IntegerField()

    def __str__(self):
        return self.name

    def get_nip(self):
        return str(self.nip)

    @property
    def get_nip_len(self):
        return len(str(self.nip))

    def get_name(self):
        return self.name

    def get_st_address(self):
        return self.st_address

    def get_city(self):
        return self.city

    def get_phone(self):
        return phone

    @property
    def phone_len(self):
        return len(str(self.phone))

class Comments(models.Model):
    company = models.ForeignKey(Companies, related_name='comment_parent', default=1)
    author = models.ForeignKey(User, related_name='comment_author', default=1)
    title = models.CharField(max_length=80, default = 'Brak tytułu ')
    text = models.TextField(default = 'pusty komentarz')
    created = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Komentarz {} dodany przez {}'.format(self.title, self.author.username)

class PdfFiles(models.Model):
    companypdf = models.FileField(upload_to='pdfs/')
    company = models.ForeignKey(Companies, related_name='pdf_parent')
