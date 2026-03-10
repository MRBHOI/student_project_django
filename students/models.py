from django.db import models

class Student(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    course = models.CharField(max_length=100)
    date_of_admission = models.DateField()

    def __str__(self):
        return f"{self.full_name} - {self.course}"

    class Meta:
        ordering = ['-date_of_admission']