from errno import EROFS
from django.db import models
from urllib import request
import re
# Create your models here.

class UserManger (models.Manager):
    def validator(self,PostData):
        errors={}
        if len(PostData.get('first_name',[]))<2:
            errors['first_name']='first name should be at least 2 characters'
        if len(PostData.get('last_name',[]))<2:
            errors['last_name']='last name should be at least 2 characters'
        if len(PostData.get('password',[]))<8:
            errors['password']='password should be at least 8 characters'
        if not PostData.get('password',[])==PostData.get('confirm_pw',[]):
            errors['confirm_pw']='Password and confirm should be match'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(PostData['email']):             
            errors['email'] = "Invalid email address!"
        
        return errors

class users(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.EmailField(unique=True)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects= UserManger()

class BookManger (models.Manager):
    def Bvalidate(self,PostData):
        errors={}
        if len(PostData['description'])<5:
            errors['description']='description should be at least 5 characters'
        return errors

class Books(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255,default='')
    uploaded_by = models.ForeignKey(users,related_name='boos_uploaded',on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(users,related_name='liked_books')
    objects= BookManger()

