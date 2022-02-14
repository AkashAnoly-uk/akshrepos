from django.shortcuts import render, redirect

import datetime as dt

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





# INSERT Project Details

def project_form(request):

    if request.method == "GET":
        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]

        # active_projects = projects.objects.filter(open_status='2022-01-29')
        
        context ={}
        context["dataset"] = projects.objects.filter(open_status='2022-01-29')
        return render(request, "employee_register/project_form.html",context)
       
    else:
        print('pos')
        form = ProjForm(request.POST)
        today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        today1 = str(today_date)
        split_a = today1.split(".")
        split_date = split_a[0]
        split_date1 = str(split_date).split(" ")
        split_daten =split_date1[0]
        projnm = request.POST['project_name']
        platname = request.POST['option_id']
        reg = projects(project_name=projnm, platform_name=platname, open_status=split_daten)
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

        # get_details = employee_details.objects.filter(pk__in=assign)
        # for datas1 in get_details:
        #     new_status = "ASSIGNED-PERSON"
        #     datas1.status = new_status
        #     datas1.save()

        
        active_emp = employee_details.objects.filter(status='Active')
        # emp_proj = projects.objects.filter(open_status='2022-01-29')
        emp_proj = projects.objects.filter(open_status=split_daten)

        assign = assignment.objects.filter(date_from=split_daten)
        empidappend = []
        

        for update_status in assign:
            empsids = update_status.employeeid
            empidappend.append(empsids)


        new_app= []

       
        for ints in empidappend:
            ints = int(ints)
            new_app.append(ints)

        # print(new_app)
        
        # exit()    


        # emp_det_id = employee_details.objects.values('full_name').filter(pk__in=empidappend)
        apppend_id = []
        active_emp_n = employee_details.objects.filter(status='Active')

        for i_d in active_emp_n:
            # print(i_d.id)
            apppend_id.append(i_d.id)

        new_apend_data = []    
            



        for (a, b) in itertools.zip_longest(new_app, apppend_id):
            if a == b:
                pass
            else:
                # print(b)
                nn = b
                # new_apend_data.nn
                # print(nn)
                new_apend_data.append(nn)


        # print(new_apend_data) 
        active_emp = employee_details.objects.filter(status='Active').filter(pk__in=new_apend_data)

        # print(active_emp)

        return render(request, "employee_register/assign_task.html",{'active_emp':active_emp, 'emp_proj':emp_proj,'date':split_daten})
      
    else:

        if request.method == 'POST':
            recomme=request.POST.getlist('interest')
            platname = request.POST['options']
     
        for index, item in enumerate(recomme):
            new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            today1 = str(new_date)
            split_a = today1.split(".")
            split_date = split_a[0]
            split_date1 = str(split_date).split(" ")
            split_daten = split_date1[0]
            survey = assignment.objects.create(employeeid=item,projectid=platname,date_from=split_daten)
           

           


        return render(request, "employee_register/assigned.html")

       
def assigned(request):
    new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
    today1 = str(new_date)
    split_a = today1.split(".")
    split_date = split_a[0]
    split_date1 = str(split_date).split(" ")
    split_daten = split_date1[0]
 
    assign = assignment.objects.filter(date_from=split_daten)
    prjappend = []
    empidappend =[]

    for update_status in assign:
        
        empsids = update_status.employeeid
        empidappend.append(empsids)
        projids = update_status.projectid
        prjappend.append(projids)
        # print(projids)




    emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=empidappend)
    
    # proj_det_id = projects.objects.filter(pk__in=prjappend)

    new_app =[]
    new_prj =[]

    for piks in prjappend:
        print(piks)
        proj_det_id = projects.objects.filter(id=piks)
        # print(proj_det_id)
        for update in proj_det_id:
            pname = update.project_name
            new_app.append(pname)
            plname = update.platform_name
            new_prj.append(plname)


    return render(request, "employee_register/assigned.html",{'emp_det':emp_det_id,'proj_name':new_app, 'pla_name':new_prj, 'date':split_daten})








                





    
    
        
        

         
        # exit()
        # result = [i for n, i in enumerate(two_lists) if i not in two_lists[:n]]  

        # apppend_id 

        # print(apppend_id)
        # print(empidappend)

        # f = lambda list1, list2: list(filter(lambda element: element not in list2, list1))

        # x = OrderedDict.fromkeys(apppend_id)
        # y = OrderedDict.fromkeys(empidappend)

        # for k in x:
        #     if k in y:
        #         x.pop(k)
        #         y.pop(k)

        # a = ["abc", "def", "ijk", "lmn", "opq", "rst", "xyz"]
        # b = ["ijk", "lmn", "opq", "rst" ]
        # b = [x for x in b if not x in a]
        # print(b)
    
        
        



        # print(x.keys())




        # print(list(active_emp))
        # exit()


       




        # print(platname)
        # exit()

        # for x, y in map(None, a, b):
    

        # recomme2 =[]
        # for checkemp in recomme:
        #     if checkemp == 'none':
        #         pass
        #     else:
        #         new_val = checkemp
        #         recomme2.append(new_val)
        

        # new_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        # today1 = str(new_date)
        # split_a = today1.split(".")
        # split_date = split_a[0]
        # split_date1 = str(split_date).split(" ")

        # for index, item in enumerate(recomme2):
            
        #     if index % 2 == 0:
        #         sk = item
        #         survey = assignment.objects.create(employeeid=sk,date_from=split_date1)
        #         survey.save() 

        #     else:
        #         prjsids = item
        #         reg = assignment.objects.all()
        #         obj = (assignment.objects.last()).id
        #         assignment.objects.filter(pk=obj).update(projectid=prjsids)

  # for update in proj_det_id:
    #     print(update.project_name)
    #     print(update.platform_name)


    # exit()    



    # proj_det_id = projects.objects.filter(pk__in=prjappend)


    # for projs in prjappend:
    #     # print(projs)
    #     proj_det= projects.objects.filter(pk__in=projs).all()
    #     print(proj_det)

    #     # for update_status in proj_det:
        #     projidsids = update_status.project_name
        #     print(projidsids)

        # projets = proj_det_id.project_name
        # print(projets)

    






    # print(proj_det_id)
    # exit()
    # print(proj_det_id.query)

    # objs = projects.objects.raw('SELECT project_name, platform_name FROM myapp_person')


    # print(proj_det_id)
    # exit()
    # # querySet1 = union(emp_det_id, proj_det_id)

    # # records = (emp_det_id | proj_det_id)

    # report = list(chain(emp_det_id, proj_det_id))
   

    # print(report)
    # exit()

    
    
  
    

    # proj_det_id = assignment.objects.filter(date_from=split_daten)

    # print(proj_det_id)
    # exit()

    # # proj = []
    # # em = []

    # for get_status in proj_det_id:
    # #     # print(get_status.employeeid)
    # #     emp_id = get_status.employeeid
    #     pro_id = get_status.projectid
    #     # print(pro_id)
    # #     # emp_det_id = employee_details.objects.values('full_name','mobile').filter(pk__in=emp_id)
    #     proj_det_id = projects.objects.values('project_name','platform_name').filter(pk__in=pro_id)
    #     print(proj_det_id)
    # # print(pro_id)    



    # exit()
   



    # assign = 

   

    





            
        




        
    


            

            
        

      
   
   


      
       
  











   


         
        







             
   

       






    






        



    
# return render(request, "employee_register/project_form.html")


# class HomePageView(ListView):
#     model = Employee
#     template_name = "employee_register/employee_form.html"






# def employee_form(request, id=0):
#     if request.method == "GET":
#         if id == 0:
#             print("--ViewPage------1-requestget method-----")
#             form = EmployeeForm()
#         else:
#             print("-----For edit function--2--------")
#             employee = Employee.objects.get(pk=id)
#             form = EmployeeForm(instance=employee)
#             # print(form)
#         return render(request, "employee_register/employee_form.html", {'form': form})
#     else:
        
#         if id == 0:
#             print("--Insert data-create----3--------")
#             form = EmployeeForm(request.POST)
#             if form.is_valid():
#                 # form.save()

#                 fulln = form.cleaned_data['full_name']
#                 mob = form.cleaned_data['mobile']
#                 proj = form.cleaned_data['projects']
#                 platf = form.cleaned_data['platform']
#                 dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
#                 # Indian_time = dt_India.strftime('%d-%b-%y %H:%M:%S')
#                 print(dt_India)
#                 today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
#                 today1 = str(today_date)
#                 split_a = today1.split(".")
#                 split_date = split_a[0]
#                 split_date1 = str(split_date).split(" ")
            
            
            
            
#                 # exit()

#                 # datestart = Indian_time
#                 # print(datestart)
#                 reg = Employee(full_name=fulln, mobile=mob, projects=proj, platform=platf, date_to=split_date1)
#                 reg.save()

    


#                 # print(fulln)
#                 # print(mob)
#                 # print(proj)
#                 # print(platf)
#                 # print(datestart)
#                 # exit()


                
         
            
            
            
                  
                
                


        #         return redirect('/employee/list')
        #     # print(form)
        #     # exit()

        # else:
        #     print("-------4-post update data-------")
        #     employee = Employee.objects.get(pk=id)
        #     form = EmployeeForm(request.POST,instance= employee)
        #     emp1 = employee.projects
        #     emp2 = employee.platform
        #     # print(employee.platform)
        #     if form.is_valid():
        #         # print(form)
        #         proj1 = form.cleaned_data['projects']
        #         plat1 = form.cleaned_data['platform']
        #     print(proj1)
        #     print(plat1)

        #         # print("=================")
            
        #     # exit()

        #     join_proj =   emp1+ ', ' + proj1
        #     join_plat =  emp2  + ', ' + plat1

        #     # print(join_proj)
        #     # print(join_plat)
        #     # exit()

        #     today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
        #     today1 = str(today_date)
        #     split_a = today1.split(".")
        #     split_date = split_a[0]
        #     split_date1 = str(split_date).split(" ")
        #     employee.projects = join_proj
        #     employee.platform = join_plat
        #     # employee.date_to = split_date1
        #     employee.from_to = split_date1
        #     employee.save()


        #     return redirect('/employee/list')    


                

                # date




                # exit()


            # fulln = form.cleaned_data['full_name']
            # mob = form.cleaned_data['mobile']
            
            # print(form)
            # exit()


            
            
            
            # platf = form.cleaned_data['platform']


            # print(form)
            # exit()

            # last_date = employee.date_to
            # last_date1 = last_date.split(" ")
            # old_date = last_date1[0]
            # print(old_date)
            # exit()

            # empformUdate = employee.projects

            # join_proj =  proj + ', ' + platf
            # print(join_proj)








            # # print(last_date1[0])


            # exit()

            # imp
         
            # today_date = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            # today1 = str(today_date)
            # split_a = today1.split(".")
            # split_date = split_a[0]
            # split_date1 = str(split_date).split(" ")


            # spl_date = split_date1[0]
            # spl_time = split_date1[1]
            # employee.projects = 
            # employee.platform = 
            # employee.from_to = split_date1
            # employee.save()


            # print(spl_date)
            # print(spl_time)

            # if 
            

            # exit()


            # employee.from_to = dt_India

            # if old_date:
            #     employee.date_to = split_date1
            #     employee.save()
                # get_todaydate =employee.date_to  
                # print(get_todaydate)
            # elif today_date:
                # pass
            


            # if today_date     
            

            # employee.save()


             # imp  


            # return redirect('/employee/list')




            # exit()




            # 
            # print(current_time) 

            # for v in form:
            #     print(v.from_to)
            # exit()   


        # print(form)
        # if form.is_valid():

            # startdate= ''

            # print(form)

            # dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            # Indian_time = dt_India.strftime('%d-%b-%y %H:%M:%S')
            # UTC_time = dt.datetime.utcnow().strftime('%d-%b-%y %H:%M:%S')
            # max_len = len(max(['UTC Time', 'Indian Time'], key=len))
            # om = Indian_time
            # print(om)



            
            


            # exit()











           

            # form.save()
        # return redirect('/employee/list')

# def employee_list(request):
#     print("-----------------u")
#     context = {'employee_list': Employee.objects.all()}
#     return render(request, "employee_register/employee_list.html", context)


# def employee_delete(request,id):
#     employee = Employee.objects.get(pk=id)
#     employee.delete()
#     return redirect('/employee/list')




    # Today Task 