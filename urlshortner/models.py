import random
from django.db import models

alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789'
size=8

def short_url_generator():
    list_short_url = []
    list_obj = URL.objects.all()
    for obj in list_obj:
        list_short_url.append(obj.short_url)
    flag = True
    while(flag):
        short_url = ''
        for i in range(size):
            short_url += random.choice(alphanum)
        if short_url not in list_short_url:
            return short_url

class URL(models.Model):
    short_url   = models.CharField(max_length=8, unique=True)
    long_url    = models.CharField(max_length=255,default='defaultlongurl')
    count       = models.IntegerField(default=0)
    active      = models.BooleanField(default=True)

    def __str__(self):
        return str(self.long_url)