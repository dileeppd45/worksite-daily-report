from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from .models import Worksite,Site, Daywisereport,Employee,Employeeattendance,UserProfileInfo

# Create your views here.
# def custom_404(request, exception):
#     return render(request, '404.html', status=404)

# def custom_403(request, exception=None):
#     return render(request, '403.html', status=403)

def first(request):
    # query = request.GET.get('search', '')
    # products = Product.objects.filter(name__icontains=query)
    # return render(request, 'first.html', {'products': products})
    return render(request, 'first.html')

@login_required
def home(request): 
    if request.method =='POST':
        siteStart =int(request.POST['start'])
        siteEnd = int(request.POST['end'])
        searchSite =request.POST.get('search','').strip()
        if(siteStart > siteEnd):
            siteStart= 1
    else:
        searchSite =request.POST.get('search','').strip()
        siteStart = 1
        siteEnd = 10
    if searchSite:
        sites = Site.objects.filter(status='active', name__icontains=searchSite)[siteStart-1:siteEnd]
    else:
        sites = Site.objects.filter(status='active')[siteStart-1:siteEnd]
    alls =[]
    for i in sites:
        s=[]
        worksites = Worksite.objects.filter(status='active',name=i.id)
        w =[]
        for j in worksites:
            reports =Daywisereport.objects.filter(status='active',worksite_name=j.id)
            r=[]
            for k in reports:
                employees =Employeeattendance.objects.filter(report=k.id)
                e=[]
                for l in employees:
                    e.append([l.employee.name,l.employee.status,l.employee.remarks,l.remarks])
                r.append([k.date,k.remarks,e])
            w.append([j.workdetails,j.startdate,j.enddate,j.workstatus,r])
        s.append([i.name,i.address,i.remarks,w,i.materials])
        alls.append(s)
    return render(request, 'home.html',{'alls':alls,'start':siteStart,'end':siteEnd,'search':searchSite})

def logoutAccount(request):
    logout(request)
    return redirect("first")

def get_reports(request, start, end):
    sites = Site.objects.filter(status='active')[start-1:end]
    
    alls =[]
    for i in sites:
        s=[]
        worksites = Worksite.objects.filter(status='active',name=i.id)
        w =[]
        for j in worksites:
            reports =Daywisereport.objects.filter(status='active',worksite_name=j.id)
            r=[]
            for k in reports:
                employees =Employeeattendance.objects.filter(report=k.id)
                e=[]
                for l in employees:
                    e.append([l.employee.name,l.employee.status,l.employee.remarks,l.remarks])
                r.append([k.date,k.remarks,e])
            w.append([j.workdetails,j.startdate,j.enddate,j.workstatus,r])
        s.append([i.name,i.address,i.remarks,w,i.materials])
        alls.append(s)

    html_table = render_to_string('reporthome.html', {'alls': alls, 'start':start})
    pdf = generate_pdf_from_html(html_table)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=site_reports.pdf'
    return response

def generate_pdf_from_html(html_table):
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html_table.encode('utf-8')), result)
    
    if not pdf.err:
        return result.getvalue()
    else:
        raise Exception('PDF generation failed')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:
                return redirect("home")
            else:
                # return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../login';</script>")
                return redirect("home")
          # Redirect to index upon successful login
        # if CustomerProfile.objects.filter(username=username, password=password).exists():
        #     a =CustomerProfile.objects.filter(username = username , password = password ).values_list('username', flat=True)
        #     print(a)
            
        #     request.session['uid']=str(a[0])
        #     return redirect('index')
        # elif CustomerProfile.objects.filter(email=username, password=password).exists():
        #     a =CustomerProfile.objects.filter(email = username , password = password ).values_list('username', flat=True)
        #     print(a)
            
        #     request.session['uid']=str(a[0])
        #     return redirect('index')
        # elif CustomerProfile.objects.filter(phone=username, password=password).exists():
        #     a =CustomerProfile.objects.filter(phone = username , password = password ).values_list('username', flat=True)
        #     print(a)
        
        #     request.session['uid']=str(a[0])
        #     return redirect('index')
        # else:
            # return HttpResponse("<script>alert('Username or Password is incorrect');window.location='../login';</script>")
    return render(request, 'login.html')

def register_request(request):
    # if request.method == 'POST':
    #     user_form = CoustomerForm(request.POST)
    #     if user_form.is_valid():
    #         try:
    #             user_form.save()
    #             return HttpResponse("<script>alert('registration successfull..');window.location='../login';</script>")
    #             return redirect(login_view)
    #         except:
    #             pass
    # else:
    #     user_form = CoustomerForm()
    # return render(request, 'register.html', {'user_form': user_form})
    return render(request, 'register.html')

def forgot_password(request):
    # if request.method == 'POST':
    #     email = request.POST['email']
    #     if CustomerProfile.objects.filter(email=email).exists():
    #         a =CustomerProfile.objects.filter(email=email ).values_list('username', flat=True)
    #         b=CustomerProfile.objects.filter(email=email ).values_list('name', flat=True)
    #         username = a[0]
    #         name=b[0]
    #         random_number = random.randint(1000, 9999)
    #         request.session['otp']=random_number
    #         receiver_email = email
    #         EMAIL_HOST = 'smtp.gmail.com'
    #         EMAIL_HOST_USER = 'workmailworkmail.w@gmail.com'
    #         EMAIL_HOST_PASSWORD = 'wdhsywhbquqohtjp'
    #         EMAIL_PORT = 587
    #         EMAIL_USE_TLS = True

    #         password = EMAIL_HOST_PASSWORD
    #         smtp_server = EMAIL_HOST
    #         sender_email = EMAIL_HOST_USER

    #         message = """\
    #                                     Subject:   OTP for Password reset conformation..

    #                                     eEarrings: hello """+str(name)+""", Use OTP """+str(random_number)+""" to reset password and use our website and donot share this code with anyone. Reset your password and discover your dezired products from us.. """
    #         context = ssl.create_default_context()
    #         with smtplib.SMTP(smtp_server, EMAIL_PORT) as server:
    #             server.ehlo()  # Can be omitted
    #             server.starttls(context=context)
    #             server.ehlo()  # Can be omitted
    #             server.login(sender_email, password)
    #             server.sendmail(sender_email, receiver_email, message)
    #         return render(request, 'forgot1.html',{'un':username,'em':email})
    #     else:
    #         return HttpResponse("<script>alert('email not found');window.location='../login';</script>")


    return render(request, 'forgot.html')

def forgot1(request):
    # if request.method=='POST':
    #     otp = request.POST['otp']
    #     un = request.POST['un']
    #     if str(request.session['otp'])==str(otp):
    #         # customer=CustomerProfile.objects.get(username=un)
    #         return render(request,'password_new.html',{'un':un})
    #     else:
    #         return HttpResponse("<script>alert('wrong otp');window.location='../login';</script>")
    return HttpResponse("<script>alert('technical error');window.location='../login';</script>")

@login_required
def add_site(request):
    siteStart = 1
    siteEnd = 10
    searchSite =request.POST.get('search','').strip()
    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        materials = request.POST['materials']
        # s=Site.objects.filter(name=name)
        # if s.exists():
        #     return HttpResponse(f"<script>alert('site same already exist'); window.location.href='/add_site';</script>")
        new_site = Site(name=name,address =address, materials=materials)
        new_site.save()
        return HttpResponseRedirect(reverse('add_site'))
    else:
        if searchSite:
            site = Site.objects.filter(status='active', name__icontains=searchSite)[siteStart-1:siteEnd]
        else:
            site = Site.objects.filter(status='active')[siteStart-1:siteEnd]
        bin = Site.objects.filter(status='bin')
        return render(request, 'add_site.html',{'sites':site,'bin':bin,'start':siteStart,'end':siteEnd,'search':searchSite})
@login_required
def searchsite(request):
    if request.method =='POST':
        siteStart =int(request.POST['start'])
        siteEnd = int(request.POST['end'])
        searchSite =request.POST.get('search','').strip()
        if(siteStart > siteEnd):
            siteStart= 1
    else:
        searchSite =request.POST.get('search','').strip()
        siteStart = 1
        siteEnd = 10
    if searchSite:
        site = Site.objects.filter(status='active', name__icontains=searchSite)[siteStart-1:siteEnd]
    else:
        site = Site.objects.filter(status='active')[siteStart-1:siteEnd]
    bin = Site.objects.filter(status='bin')
    return render(request, 'add_site.html',{'sites':site,'bin':bin,'start':siteStart,'end':siteEnd,'search':searchSite})

@login_required
def editSite(request,siteid):
    try:
        employee = Site.objects.get(id=siteid,status='active')
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_site';</script>")
    if request.method == 'POST':
        employee.address= request.POST['address'] 
        employee.remarks = request.POST['remarks']
        employee.name = request.POST['name']
        employee.materials = request.POST['materials']
        employee.save()
        return HttpResponse(f"<script>alert('Updated Site'); window.location.href='/add_site';</script>")
    else:
        
        return render(request, 'edit_site.html',{'employee':employee})

@login_required
def binSite(request,siteid):
    try:
        employee = Site.objects.get(id=siteid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_site';</script>")
    if employee.status == 'active':
        employee.status = 'bin'
        employee.save()
        return HttpResponse(f"<script>alert('Removed site to Recycle Bin'); window.location.href='/add_site';</script>")
    if employee.status =='bin':
        return HttpResponse(f"<script>alert('Already removed to Recycle Bin'); window.location.href='/add_site';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_site';</script>")

@login_required
def recycleSite(request,siteid):
    try:
        employee = Site.objects.get(id=siteid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_site';</script>")
    if employee.status == 'bin':
        employee.status = 'active'
        employee.save()
        return HttpResponse(f"<script>alert('Restored Site'); window.location.href='/add_site';</script>")
    if employee.status =='active':
        return HttpResponse(f"<script>alert('Already restored'); window.location.href='/add_site';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_site';</script>")

@login_required
def deleteSite(request, siteid):
    try:
        site = Site.objects.get(id=siteid)
    except Site.DoesNotExist:
        return HttpResponse("<script>alert('404 error'); window.location.href='/add_site';</script>")

    # If the user submits the verification form
    if request.method == "POST" and request.POST.get("confirm") == "yes":
        pin = str(request.POST['pin'])
        if pin !='0987':
            return HttpResponse("<script>alert('Wrong pin..'); window.location.href='/add_site';</script>")
        if site.status == "bin":
            site.status = "deleted"
            site.save()
            return HttpResponse("<script>alert('Deleted Site Permanently'); window.location.href='/add_site';</script>")
        elif site.status == "active":
            return HttpResponse("<script>alert('404 error'); window.location.href='/add_site';</script>")
        elif site.status == "deleted":
            return HttpResponse("<script>alert('Site Already Deleted'); window.location.href='/add_site';</script>")
    else:
        # Redirect to the verification page
        return render(request, "user_verification.html", {"site": site})

@login_required
def add_work(request,siteid):
    site =Site.objects.get(id=siteid)
    if request.method == 'POST':
        workdetails = request.POST['workdetails']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        workstatus = request.POST['workstatus']
        new_site = Worksite(name=site, workdetails=workdetails, startdate = startdate, enddate = enddate, workstatus =workstatus)
        new_site.save()
        return redirect('add_work', siteid=siteid)
    
    else:
        site =Site.objects.get(id=siteid)
        worksites =Worksite.objects.filter(name = site.id,status ='active')
        bin = Worksite.objects.filter(name = site.id,status ='bin')
        return render(request, 'add_work.html',{'worksites':worksites,'site':site,'id':siteid,'bin':bin})

@login_required
def editWork(request,workid,siteid):
    try:
        employee = Worksite.objects.get(id=workid,status='active')
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")
    if request.method == 'POST':
        employee.workdetails= request.POST['workdetails'] 
        employee.startdate = request.POST['startdate']
        employee.enddate = request.POST['enddate']
        employee.workstatus = request.POST['workstatus']
        employee.save()
        return HttpResponse(f"<script>alert('Updated Work'); window.location.href='/add_work/{siteid}';</script>")
    else:
        startdate = employee.startdate.strftime('%Y-%m-%d')
        enddate = employee.enddate.strftime('%Y-%m-%d')
        return render(request, 'edit_work.html',{'employee':employee,'id':workid,'startdate':startdate,'enddate':enddate})

@login_required
def binWork(request,workid,siteid):
    try:
        employee = Worksite.objects.get(id=workid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status == 'active':
        employee.status = 'bin'
        employee.save()
        return HttpResponse(f"<script>alert('Removed Work to Recycle Bin'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status =='bin':
        return HttpResponse(f"<script>alert('Already removed to Recycle Bin'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")

@login_required
def recycleWork(request,workid,siteid):
    try:
        employee = Worksite.objects.get(id=workid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status == 'bin':
        employee.status = 'active'
        employee.save()
        return HttpResponse(f"<script>alert('Restored Work'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status =='active':
        return HttpResponse(f"<script>alert('Already restored'); window.location.href='/add_work/{siteid}';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")

@login_required
def deleteWork(request,workid,siteid):
    try:
        employee = Worksite.objects.get(id=workid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")
    if request.method == "POST" and request.POST.get("confirm") == "yes":
        pin = str(request.POST['pin'])
        if pin !='0987':
            return HttpResponse(f"<script>alert('Wrong pin..'); window.location.href='/add_work/{siteid}';</script>")
        if employee.status == 'bin':
            employee.status = 'deleted'
            employee.save()
            return HttpResponse(f"<script>alert('Deleted Work Permenently'); window.location.href='/add_work/{siteid}';</script>")
        if employee.status =='active':
            return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_work/{siteid}';</script>")
        if employee.status =='deleted':
            return HttpResponse(f"<script>alert('Work Already Deleted'); window.location.href='/add_work/{siteid}';</script>")
    else:
        # Redirect to the verification page
        return render(request, "user_verification_work.html", {"site": employee,"id":siteid})

@login_required
def add_report(request,worksiteid):
    site =Worksite.objects.get(id=worksiteid)
    if request.method == 'POST':
        date = request.POST['date']
        s = Daywisereport.objects.filter(worksite_name=site, date=date)
        if s.exists():
            return HttpResponse(f"<script>alert('work having same date report already exist'); window.location.href='/add_report/{worksiteid}';</script>")
        new_site = Daywisereport(worksite_name=site, date=date)
        new_site.save()
        return redirect('add_report', worksiteid=worksiteid)
    else:
        site =Worksite.objects.get(id=worksiteid)
        worksites =Daywisereport.objects.filter(worksite_name = site.id, status='active')
        binworksites =Daywisereport.objects.filter(worksite_name = site.id, status='bin')
        return render(request, 'add_report.html',{'reports':worksites,'bin':binworksites,'site':site,'id':worksiteid})

@login_required
def editReport(request,reportid,workid):
    try:
        employee = Daywisereport.objects.get(id=reportid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")
    if request.method == 'POST':
        remarks = request.POST['remarks']
        employee.remarks=remarks
        employee.save()
        return HttpResponse(f"<script>alert('Updated Reports Remark'); window.location.href='/add_report/{workid}';</script>")
    else:
        return render(request, 'edit_report.html',{'employee':employee,'id':workid})

@login_required
def binReport(request,reportid,workid):
    try:
        employee = Daywisereport.objects.get(id=reportid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")
    if employee.status == 'active':
        employee.status = 'bin'
        employee.save()
        return HttpResponse(f"<script>alert('Removed Report to Recycle Bin'); window.location.href='/add_report/{workid}';</script>")
    if employee.status =='bin':
        return HttpResponse(f"<script>alert('Already removed to Recycle Bin'); window.location.href='/add_report/{workid}';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")

@login_required
def recycleReport(request,reportid,workid):
    try:
        employee = Daywisereport.objects.get(id=reportid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")
    if employee.status == 'bin':
        employee.status = 'active'
        employee.save()
        return HttpResponse(f"<script>alert('Restored Report'); window.location.href='/add_report/{workid}';</script>")
    if employee.status =='active':
        return HttpResponse(f"<script>alert('Already restored'); window.location.href='/add_report/{workid}';</script>")
    if employee.status =='deleted':
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")

@login_required
def deleteReport(request,reportid,workid):
    try:
        employee = Daywisereport.objects.get(id=reportid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")
    if request.method == "POST" and request.POST.get("confirm") == "yes":
        pin = str(request.POST['pin'])
        if pin !='0987':
            return HttpResponse(f"<script>alert('Wrong pin..'); window.location.href='/add_report/{workid}';</script>")
        if employee.status == 'bin':
            employee.status = 'deleted'
            employee.save()
            return HttpResponse(f"<script>alert('Deleted Report Permenently'); window.location.href='/add_report/{workid}';</script>")
        if employee.status =='active':
            return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_report/{workid}';</script>")
        if employee.status =='deleted':
            return HttpResponse(f"<script>alert('Report Already Deleted'); window.location.href='/add_report/{workid}';</script>")
    else:
        # Redirect to the verification page
        return render(request, "user_verification_report.html", {"site": employee,"id":workid})


@login_required
def add_workers(request,dayreportid):
    site =Daywisereport.objects.get(id=dayreportid)
    if request.method == 'POST':
        employee = request.POST['employee']
        emp = Employee.objects.get(id =employee)
        # attendance = request.POST['attendance']
        attendance ="Present"
        remark =request.POST['remark']
        s = Employeeattendance.objects.filter(report=site,employee=emp)
        if s.exists():
            att = Employeeattendance.objects.get(report=site,employee=emp)
            att.attendance =attendance
            att.remarks = remark
            att.save()
            return redirect('add_workers', dayreportid=dayreportid)

        new_site = Employeeattendance(report=site, employee=emp, attendance=attendance,remarks=remark)
        new_site.save()
        return redirect('add_workers', dayreportid=dayreportid)
    else:
        site =Daywisereport.objects.get(id=dayreportid)
        worksites =Employeeattendance.objects.filter(report = site.id)
        employee =Employee.objects.filter(status='in')
        return render(request, 'add_workers.html',{'employees':worksites,'site':site,'employee':employee,'id':dayreportid})

@login_required
def RemoveWorker(request,workerid,id):
    try:
        employee = Employeeattendance.objects.get(id=workerid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_workers/{id}';</script>")
    employee.delete()
    return HttpResponse(f"<script>alert('Removed'); window.location.href='/add_workers/{id}';</script>")

@login_required
def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        remarks = request.POST['remarks']
        new_site = Employee(name=name,remarks = remarks)
        new_site.save()
        return HttpResponseRedirect(reverse('add_employee'))
    else:
        employee = Employee.objects.filter(status='in')
        removed = Employee.objects.filter(status='not in')
        return render(request, 'add_employee.html',{'employees':employee,'removed':removed})

@login_required
def editEmployee(request,empid):
    try:
        employee = Employee.objects.get(id=empid)
    except:
        return HttpResponse(f"<script>alert('404 error'); window.location.href='/add_employee';</script>")
    if request.method == 'POST':
        name = request.POST['name']
        remarks = request.POST['remarks']
        employee.status = request.POST['status']
        employee.name =name
        employee.remarks=remarks
        employee.save()
        return HttpResponse(f"<script>alert('Updated Employee Details'); window.location.href='/add_employee';</script>")
    else:
        return render(request, 'edit_employee.html',{'employee':employee})

        

        


    
