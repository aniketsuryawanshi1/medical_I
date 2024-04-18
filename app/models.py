from django.db import models

# Create your models here.

class MedicalInsuranceCost(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    smoker = models.CharField(max_length=10)
    bmi = models.FloatField()
    children = models.IntegerField()
    region = models.CharField(max_length=30)
