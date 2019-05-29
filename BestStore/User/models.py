from django.db import models

# Create your models here.


class ContactQuery(models.Model):
    name = models.CharField(max_length=60, null=True)
    email = models.EmailField(max_length=50, null=True)
    subject = models.CharField(max_length=30, null=True)
    query = models.TextField()
