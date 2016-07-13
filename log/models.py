from django.db import models

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
    text = models.TextField()
    parent_id = models.ForeignKey(Companies)
