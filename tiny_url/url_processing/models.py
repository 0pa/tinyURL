from django.db import models


class Url(models.Model):
    tiny_url = models.CharField(max_length=10, primary_key=True)
    original_url = models.CharField(max_length=300)
    counter = models.IntegerField(default=0)
    created_date = models.DateTimeField('date published')
    last_request_date = models.DateTimeField('last seen date')
