from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, unique=True)

    def __str__(self):
        return self.user.username

class Site(models.Model):
    name=models.CharField(max_length=255,null=True)
    address =models.CharField(max_length=500,null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    c_date =models.DateField(auto_now_add=True)
    c_time = models.TimeField(auto_now=True)
    materials=models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}({self.address})"
    class Meta:
        ordering = ['-id'] 

class Worksite(models.Model):
    WORK_STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Delayed', 'Delayed'),
    ]
    name = models.ForeignKey(Site,on_delete=models.CASCADE)
    workdetails=models.CharField(max_length=1000,null=True)
    startdate = models.DateField()
    enddate = models.DateField()
    workstatus = models.CharField(max_length=200, choices=WORK_STATUS_CHOICES, default='Not Started')
    def __str__(self):
        return f"{self.name.name}({self.startdate}-{self.enddate})({self.workstatus})"
    status =models.CharField(default='active', max_length=50)
    class Meta:
        ordering = ['-id'] 


class Employee(models.Model):
    name = models.CharField(max_length=255)
    remarks = models.CharField(max_length=1005, blank=True, null=True)
    status =models.CharField(default='in', max_length=50)
    def __str__(self):
        return self.name
    
    
class Daywisereport(models.Model):
    worksite_name = models.ForeignKey(Worksite, on_delete=models.CASCADE)
    date = models.DateField()
    remarks = models.CharField(max_length=1005, blank=True, null=True)    
    status =models.CharField(default='active', max_length=50)
    

class Employeeattendance(models.Model):
    report = models.ForeignKey(Daywisereport, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    #limit_choices_to={'status': 'in'}
    attendance = models.CharField(max_length=10, choices=[('Precent', 'Present'), ('Absent', 'Absent'), ('Leave', 'Leave')])
    remarks = models.CharField(max_length=255, blank=True, null=True)
    

