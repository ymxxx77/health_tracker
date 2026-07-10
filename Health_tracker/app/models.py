from django.db import models
from django.contrib.auth.models import User

class ExerciseRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.CharField(max_length=50)
    duration = models.IntegerField()
    calories_burned = models.IntegerField()

class DietRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal = models.CharField(max_length=50)
    food = models.CharField(max_length=100)
    calories = models.IntegerField()