from django.db import models
from django.forms import DateTimeField

# Create your models here.
class student(models.Model):
    Full_Name=models.CharField(max_length=255)
    Email=models.EmailField(unique=True)
    Phone=models.CharField(max_length=13)
    Course=models.CharField(max_length=255)
    Date_of_Admission=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Full_Name   