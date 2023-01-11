from django.db import models
# from storage import OverwriteStorage

# Create your models here.
# models.py
# class Image(models.Model):
# 	sudoku_Img = models.ImageField(upload_to='static/sudokuDIP/images/')
# from django.db import models
class Image(models.Model):
    file = models.ImageField(upload_to='image/')
    date = models.DateTimeField(auto_now_add =True)