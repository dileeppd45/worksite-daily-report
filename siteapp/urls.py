from . import views
from django.urls import path

urlpatterns = [
    path('', views.login_view, name='first'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logoutAccount, name='logout'),
    path("register/", views.register_request, name="register"),
    path("forgot", views.forgot_password, name="forgot"),
    path("forgot1",views.forgot1),
    path('home/', views.home, name='home'),
    path('get_reports/<int:start>/<int:end>', views.get_reports, name='get_reports'),

    
    path('add_site/', views.add_site, name='add_site'),
    path('searchsite', views.searchsite, name='searchsite'),
    path('editSite/<int:siteid>', views.editSite, name='editSite'),
    path('binSite/<int:siteid>', views.binSite, name='binSite'),
    path('recycleSite/<int:siteid>', views.recycleSite, name='recycleSite'),
    path('deleteSite/<int:siteid>', views.deleteSite, name='deleteSite'),


    path('add_employee/', views.add_employee, name='add_employee'),
    path('editEmployee/<int:empid>', views.editEmployee, name='editEmployee'),

    path('add_work/<int:siteid>',views.add_work, name='add_work'),
    path('editWork/<int:workid>/<int:siteid>',views.editWork, name='editWork'),
    path('binWork/<int:workid>/<int:siteid>',views.binWork, name='binWork'),
    path('recycleWork/<int:workid>/<int:siteid>',views.recycleWork, name='recycleWork'),
    path('deleteWork/<int:workid>/<int:siteid>',views.deleteWork, name='deleteWork'),


    path('add_report/<int:worksiteid>',views.add_report, name='add_report'),
    path('editReport/<int:reportid>/<int:workid>',views.editReport, name='editReport'),
    path('binReport/<int:reportid>/<int:workid>',views.binReport, name='binReport'),
    path('recycleReport/<int:reportid>/<int:workid>',views.recycleReport, name='recycleReport'),
    path('deleteReport/<int:reportid>/<int:workid>',views.deleteReport, name='deleteReport'),


    path('add_workers/<int:dayreportid>',views.add_workers, name='add_workers'),
    path('RemoveWorker/<int:workerid>/<int:id>', views.RemoveWorker, name='RemoveWorker'),
]