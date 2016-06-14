from django.db import models

# Create your models here.
class Companies(models.Model):
    name = models.CharField(max_length=70)
    nip = models.IntegerField()

    def __str__(self):
        return self.name

    def get_nip(self):
        return str(self.nip)

    @property
    def get_nip_len(self):
        return len(str(self.nip))

    def get_name(self):
        return self.name
