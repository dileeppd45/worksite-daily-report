from django.contrib import admin
from .models import  Worksite,Employee,Site,UserProfileInfo,Daywisereport,Employeeattendance



admin.site.register(Site)
admin.site.register(Worksite)
admin.site.register(Employee)
admin.site.register(UserProfileInfo)
admin.site.register(Employeeattendance)


admin.site.register(Daywisereport)