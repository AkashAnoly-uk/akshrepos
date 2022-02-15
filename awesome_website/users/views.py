from django.shortcuts import render, redirect

import datetime as dt
import datetime

from .forms import ProjForm
from .forms import CheckForm
from .models import projects
from .models import employee_details
from .models import assignment
from django.http import HttpResponse
from django.core import serializers
from itertools import chain
from collections import OrderedDict
import itertools 
import json
from time import gmtime, strftime





# INSERT Project Details

def project_form(request):

    if request.method == "GET":
        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]


        emp_projs = projects.objects.all()

        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status


            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                
            else:
                pass

        id_filter = projects.objects.filter(pk__in=new_updatestes)

        # reg = projects.objects.all()
        # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        # today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        # print(today_min)
        # print(today_max)
        # exit()
        # get = projects.objects.filter(open_status__gte=today_min)
        # active_projects = projects.objects.filter(open_status='2022-01-29')

        # context ={}
        # context["dataset"] = projects.objects.filter(open_status__gte='2022-02-05 09:16:57').filter(open_status__lte='2022-02-05 09:20:49')
        return render(request, "employee_register/project_form.html",{'emp_proj':id_filter})
   
    else:

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]
        projnm = request.POST['project_name']
        platname = request.POST['option_id']
        reg = projects(project_name=projnm, platform_name=platname, open_status=split_date)
        reg.save()

        return render(request, "employee_register/project_form.html")



# Employee Active and Inactive Task

def empoyee_check(request):
    if request.method == "GET":
        context ={}
        context["dataset"] = employee_details.objects.filter(status='Active')
        return render(request, "employee_register/empoyee_check.html", context)
        
    else:
        if request.method == 'POST':
            recommendations=request.POST.getlist('recommendations')
            emp_id = employee_details.objects.filter(pk__in=recommendations)

            for update_status in emp_id:
                new_status = "IN-ACTIVE"

                update_status.status = new_status
                update_status.save()

    
        # return render(request, "employee_register/check_inac.html")
        return redirect('/employee/check_inac')
         
def check_inac(request):
    context = {}
    context['dataset'] = employee_details.objects.filter(status="IN-ACTIVE")
    return render(request, "employee_register/check_inac.html",context)

           

           
# Assining task details
    
def assign_task(request):
    if request.method == "GET":

        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]


        assign = assignment.objects.values_list('employeeid', flat=True)
        
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))
        # print(yesterday_min)
        # exit()


       
        # active_emp = employee_details.objects.filter(status='Active')
        # emp_proj = projects.objects.filter(open_status='2022-01-29')

        # ---------------------todays_task----start---------------------
       
        
        emp_projs = projects.objects.all()

    
        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status


            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                

            else:
                pass

             
      
                

        id_filter = projects.objects.filter(pk__in=new_updatestes)  



        #------------------TODAY TASKS-------completee--------------- 

        assign = assignment.objects.filter(date_from__gte=today_min)

        assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min)

       

        proj_idds = []

        for update_s in assign_yestday:
            pro_ids = update_s.projectid
            proj_idds.append(pro_ids)

        pro_app= []

        for projs in proj_idds:
            pro_in = int(projs)
            pro_app.append(pro_in)

        empidappend = []

        for update_status in assign:
            empsids = update_status.employeeid
            empidappend.append(empsids)

        new_app= []

       
        for ints in empidappend:
            ints = int(ints)
            new_app.append(ints)

            # -------------------------------------------

        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active').filter(role='IA')
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

        

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)

        new_apend_data = [] 

        difference = set(new_app).symmetric_difference(set(apppend_id))
        list_difference = list(difference)
        count_person = len(list_difference)
 
 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)

        return render(request, "employee_register/assign_task.html",{'active_emp':active_emp,'active_tl':active_tl ,'emp_proj':id_filter,'date':split_daten,'count':count_person})

   
      
    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']
            tl_id = request.POST['option_tl']
            # print(tl_id)
            # exit()

    

            for index, item in enumerate(recomme):
                new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                today1 = str(new_date)
                split_a = today1.split(".")
                split_date = split_a[0]
                split_date1 = str(split_date).split(" ")
                split_daten = split_date1[0]
                survey = assignment.objects.create(employeeid=item,projectid=platname,date_from=split_date,tl_id=tl_id)
       

            return render(request, "employee_register/assigned.html")


def reassign_task(request):
    if request.method == "GET":
        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
     
        assign = assignment.objects.filter(date_from__gte=today_min)
        prjappend = []
        empidappend =[]

        for update_status in assign:
            
            empsids = update_status.employeeid
            empidappend.append(empsids)
            projids = update_status.projectid
            prjappend.append(projids)


            

        emp_det_id = employee_details.objects.values('id','full_name','mobile').filter(pk__in=empidappend)

        # print(emp_det_id)
        # exit()

 
        emp_projs = projects.objects.all()

    
        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status


            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                

            else:
                pass

             
      
                

        id_filter = projects.objects.filter(pk__in=new_updatestes)  



        #------------------TODAY TASKS-------completee--------------- 

        assign = assignment.objects.filter(date_from__gte=today_min)

        # assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min)

       

       

        empidappend = []

        for update_status in assign:
            empsids = update_status.employeeid
            # emps_ids = update_status.employeeid
            empidappend.append(empsids)
            # if 

        new_app= []

       
        for ints in empidappend:
            ints = int(ints)
            new_app.append(ints)


        # print(new_app)
        # exit()    

        # emp_chk =[]




            

     

            # -------------------------------------------

        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active').filter(role='IA')
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

        

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)

        new_apend_data = [] 

        difference = set(new_app).symmetric_difference(set(apppend_id))
        list_difference = list(difference)
        count_person = len(list_difference)
 
 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=new_app)

 
        return render(request, "employee_register/reassign_task.html",{'emp_det':active_emp,'active_tl':active_tl ,'emp_proj':id_filter, 'date':split_daten})

    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']
            tl_id = request.POST['option_tl']
         
            for index, item in enumerate(recomme):
                new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                today1 = str(new_date)
                split_a = today1.split(".")
                split_date = split_a[0]
                split_date1 = str(split_date).split(" ")
                split_daten = split_date1[0]
                survey2 = assignment.objects.create(employeeid=item,projectid=platname,from_to=split_date,tl_id=tl_id)
                survey2.save()
            
            return render(request, "employee_register/assigned.html")


def assign_previous(request):
    if request.method == "GET":

        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]


         
        assign = assignment.objects.values_list('employeeid', flat=True)
        
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)

        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))
        # print(yesterday)
        # exit()

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))
        # print(yesterday_min)
        # exit()

        srt_paqtmax = str(today_max)
        split_partmax = srt_paqtmax.split(' ')
        split_partmax[0] = yesterday
        yesterday_max = " ".join(map(str,split_partmax))
   

        # ---------------------todays_task----start---------------------
       
        
        emp_projs = projects.objects.all()

        new_updatestes = []

        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status


            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                

            else:
                pass

        id_filter = projects.objects.filter(pk__in=new_updatestes)  



        #------------------TODAY TASKS-------completee--------------- 

        assign_today = assignment.objects.filter(date_from__gte=today_min)

        assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(date_from__lte=yesterday_max)
   
        proj_idds = []

        for update_s in assign_yestday:
            pro_ids = update_s.projectid
            proj_idds.append(pro_ids)

        pro_app= []

        for projs in proj_idds:
            pro_in = int(projs)
            pro_app.append(pro_in)

        empidappend = []

        for update_status in assign_today:
            empsids = update_status.employeeid
            empidappend.append(empsids)


        emptody_app= []

       
        for ints in empidappend:
            ints = int(ints)
            emptody_app.append(ints)
     
  

            # -------------------------------------------

        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active').filter(role="IA")
        active_tl = employee_details.objects.filter(status='Active').filter(role='TL')

        for i_d in active_emp_n:
          
            apppend_id.append(i_d.id)


        new_apend_data = [] 

        difference = set(emptody_app).symmetric_difference(set(apppend_id))
        list_difference = list(difference)

 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=list_difference)

        return render(request, "employee_register/assign_previous.html",{ 'emp_proj':id_filter,'date':yesterday})

    else:
        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']

   
        new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(new_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten = split_date1[0]    

        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
       
        today = datetime.datetime.utcnow().date()

        yesterday = str(today - datetime.timedelta(days=1))

        srt_paqt = str(today_min)
        split_part = srt_paqt.split(' ')
        split_part[0] = yesterday
        yesterday_min = " ".join(map(str,split_part))

        if len(recomme) == 0:

            assign_yestday = assignment.objects.filter(date_from__gte=yesterday_min).filter(projectid=platname)
            emy_id =[]
            for update_e in assign_yestday:
                empsids = update_e.employeeid
                emy_id.append(empsids)

            active_emp_yesterday = employee_details.objects.filter(pk__in=emy_id)

            

            active_emp_today = assignment.objects.filter(date_from__gte=today_min).filter(projectid=platname)
  
            emp_yest = []


            for stat_e in active_emp_yesterday:
                emp_ids = stat_e.id
                emp_yest.append(emp_ids)

            emptoday = []

            for stat_u in active_emp_today:
                emp_tody = stat_u.employeeid
                emptoday.append(emp_tody)
            
            emptoday_n = []    
            for ints in emptoday:
                ints = int(ints)
                emptoday_n.append(ints)
            
            difference = set(emp_yest).symmetric_difference(set(emptoday_n))
            list_difference = list(difference)
            emp_projs = projects.objects.filter(open_status__gte=today_min)
           
        
            new_updatestes = []
            for n_update in emp_projs:
                open_o = n_update.open_status 
                close_o = n_update.close_status
                if open_o and close_o == '':
                    open_d = n_update.id
                    new_updatestes.append(open_d)
                    
                else:
                    pass

            listsss =[platname]
        

                
            id_filter = projects.objects.filter(pk__in=listsss)
            active_tl = employee_details.objects.filter(status='Active').filter(role='TL')
        

            active_emp = employee_details.objects.filter(pk__in=list_difference)
            platform_proj = projects.objects.filter(pk__in=listsss)
            

            return render(request, "employee_register/assign_previousdata.html",{'active_emp':active_emp,'active_tl':active_tl,'emp_proj':id_filter,'date':yesterday})
      
        else:
            if request.method == 'POST':

                recomme=request.POST.getlist('interest')
                platname = request.POST['options']
                tl_id = request.POST['option_tl']
            

                for index, item in enumerate(recomme):
                    new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                    today1 = str(new_date)
                    split_a = today1.split(".")
                    split_date = split_a[0]
                    split_date1 = str(split_date).split(" ")
                    split_daten = split_date1[0]
                    survey = assignment.objects.create(employeeid=item,projectid=platname,date_from=split_date,tl_id=tl_id)
           

            return render(request, "employee_register/assigned.html")            


       
def assigned(request):
    new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today1 = str(new_date)
    split_a = today1.split(".")
    split_date = split_a[0]
    split_date1 = str(split_date).split(" ")
    split_daten = split_date1[0]
    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
 
    assign = assignment.objects.filter(date_from__gte=today_min)

    empidappend =[]
    prjappend = []
    tl_ides = []

    for update_status in assign:
        
        empsids = update_status.employeeid
        empidappend.append(empsids)
        projids = update_status.projectid
        prjappend.append(projids)
        tl_part = update_status.tl_id
        tl_ides.append(tl_part)
    


    emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend)

    new_app =[]
    new_prj =[]
    tl_fulname =[]

    for piks in prjappend:
      
        proj_det_id = projects.objects.filter(id=piks)
        
        for update in proj_det_id:
            pname = update.project_name
            new_app.append(pname)
            plname = update.platform_name
            new_prj.append(plname)
    for tls in tl_ides:
      
        tl_idfs = employee_details.objects.filter(id=tls)
     
        for up_tl in tl_idfs:
            tl_name = up_tl.full_name
            tl_fulname.append(tl_name)
   


    # ------------------------------------Ressign part-----------------------------------
    assignment2 = assignment.objects.filter(from_to__gte=today_min)

    empidap =[]
    projap = []

    for upd_status in assignment2:
        
        emp_id = upd_status.employeeid
        empidap.append(emp_id)
        proj_id = upd_status.projectid
        projap.append(proj_id) 



    
    ressignm_det = employee_details.objects.values('full_name','mobile').filter(pk__in=empidap)


    se_proj =[]
    se_plat =[]

    for pi_ks in projap:
        # print(piks)
        proj_de_id = projects.objects.filter(id=pi_ks)
        
        for update_a in proj_de_id:
            pname = update_a.project_name
            se_proj.append(pname)
            plname = update_a.platform_name
            se_plat.append(plname)


    return render(request, "employee_register/assigned.html",{'emp_det':emp_det_id,'proj_name':new_app,'pla_name':new_prj,'ressignm_det':ressignm_det,'se_proj':se_proj,'se_plat':se_plat,'date':split_daten, 'tl_fulname':tl_fulname})



def project_close(request):

    if request.method == "GET":

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]

        
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]

        # context ={}
        # context["dataset"] = projects.objects.filter(open_status__gte=today_min)

        
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        emp_projs = projects.objects.all()
        new_updatestes = []


        for n_update in emp_projs:
            open_o = n_update.open_status
            close_o = n_update.close_status

            if len(open_o) != 0 and len(close_o) ==0:
                open_d = n_update.id
                new_updatestes.append(open_d)
                

            else:
                open_d = n_update.id
                print(open_d)
                

        id_filter = projects.objects.filter(pk__in=new_updatestes)


        return render(request, "employee_register/project_close.html",{'dataset':id_filter})
        
    else:
      

        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        projnm = request.POST['option_close']

        types_chng = int(projnm)

        # today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        
        emp_det = projects.objects.all()
        new_apps = []

        for update_time in emp_det:
            idps = update_time.id
            
            if idps == types_chng:
                
                update_time.close_status = split_date
                update_time.save()
            else:
                pass
   
        return render(request, "employee_register/project_close.html")        


# https://www.youtube.com/watch?v=JVFH8fuR4l0
# https://www.youtube.com/watch?v=JVFH8fuR4l0

# https://www.youtube.com/watch?v=qSjSn620vhI
# Newparts

# chmod 400 ec2_key.pem        

# ssh -i "akash_e2c_key.pem" ubuntu@ec2-52-22-227-158.compute-1.amazonaws.com


# CREATE USER 'root'@'%' IDENTIFIED BY 'root';
# GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;

# sudo apt-get update

# sudo apt-get install php-fpm php-mysqlhttps://github.com/AkashAnoly-uk/employee/commits?author=AkashAnoly-uk

# sudo apt install mysql-server

# sudo /etc/init.d/apache2 restart

# sudo service apache2 status
# sudo apt-get install php-fpm php-mysql
# sudo apt-get install phpmyadmin
# sudo apt-get install libapache2-mod-php
# sudo ln -s /usr/share/phpmyadmin /var/www/html
# sudo systemctl restart nginx

# sudo nano /etc/nginx/sites-available/default
# sudo systemctl reload nginx
# sudo ln -s /usr/share/phpmyadmin /var/www/html


# CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
# GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'localhost';

# rm -r akashemps


# sudo apt install git-all
# FLUSH PRIVILEGES;



# sudo ln -s /usr/share/phpmyadmin /var/www/52.22.227.158/phpmyadmin

# https://stackoverflow.com/questions/68775869/support-for-password-authentication-was-removed-please-use-a-personal-access-to

# github_token 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

# git remote add origin ssh://git@github.com:AkashAnoly-uk/employee.git

# git remote set-url origin https://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@github.com/AkashAnoly-uk/employee.git

# git@github.com:AkashAnoly-uk/employee.git

# git remote set-url origin https://github.com/AkashAnoly-uk/employee.git
                            # https://github.com/AkashAnoly-uk/employee

# git remote set-url origin https://scuzzlebuzzle:<MYTOKEN>@github.com/scuzzlebuzzle/ol3-1.git

# git remote set-url origin ssh://git@github.com:AkashAnoly-uk/akshrepos.git



                            # git remote add origin ssh://github.com/AkashAnoly-uk/akashemps
                            # git remote add origin ssh://github.com:AkashAnoly-uk/akshrepos.git
                            # git clone git@github.com:AkashAnoly-uk/akashemps.git
                            # git clone git@github.com:AkashAnoly-uk/employee.git
                            # git clone git@github.com:Utshuk/Django.git


                            # git remote add origin ssh://github.com/AkashAnoly-uk/akashemps

                            # git remote add origin ssh://git@github.com:AkashAnoly-uk/employee.git


                            # git clone https://github.com/AkashAnoly-uk/employee.git
                           #  https://github.com/AkashAnoly-uk/employee.git
                           # git clone https://github.com/AkashAnoly-uk/employee/tree/master

                            # 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

                            # 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  akashDjango new tokkens

# sudo mysql -p -u root

# CREATE USER 'USERNAME'@'%' IDENTIFIED BY 'PASSWORD';
# GRANT ALL PRIVILEGES ON *.* TO 'USERNAME'@'%' WITH GRANT OPTION;

# sudo mysql -u root;
# use mysql;
# UPDATE mysql.user SET plugin = 'mysql_native_password', Password = PASSWORD('pass1234') WHERE User = 'root';
# FLUSH PRIVILEGES;
# exit;


# UPDATE user SET Password='root' WHERE User='root'; FLUSH PRIVILEGES; exit;


   




    



            
  


    


                

        

    
   





               

        

    

    




    





