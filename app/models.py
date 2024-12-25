from django.db import models

class Designation(models.Model):
    job=models.CharField(max_length=100)
    def __str__(self):
        return self.job
    
class Users(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    job=models.ForeignKey(Designation,on_delete=models.CASCADE,related_name="designation",null=True,blank=True)
