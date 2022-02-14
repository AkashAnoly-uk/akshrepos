from django.shortcuts import render, redirect
from django.views.generic import ListView# new
from django.urls import reverse_lazy # new
from .forms import EmployeeForm
from .models import Employee
# from datetime import date
# from datetime import datetime
import datetime as dt
# import datetime 
# Create your views here.

# class HomePageView(ListView):
#     model = Employee
#     template_name = "employee_register/employee_form.html"






def employee_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            print("--ViewPage------1-requestget method-----")
            form = EmployeeForm()
        else:
            print("-----For edit function--2--------")
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(instance=employee)
            print(form)
        return render(request, "employee_register/employee_form.html", {'form': form})
    else:
        
        if id == 0:
            print("--Insert data-----3--------")
            form = EmployeeForm(request.POST)
            if form.is_valid():
                # form.save()

                fulln = form.cleaned_data['full_name']
                mob = form.cleaned_data['mobile']
                proj = form.cleaned_data['projects']
                platf = form.cleaned_data['platform']
                dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
                # Indian_time = dt_India.strftime('%d-%b-%y %H:%M:%S')
                print(dt_India)
                # exit()

                # datestart = Indian_time
                # print(datestart)
                reg = Employee(full_name=fulln, mobile=mob, projects=proj, platform=platf, date_to=dt_India)
                reg.save()

    


                # print(fulln)
                # print(mob)
                # print(proj)
                # print(platf)
                # print(datestart)
                # exit()


                
         
            
            
            
                  
                
                


                return redirect('/employee/list')
            # print(form)
            # exit()

        else:
            print("-------4-post update data-------")
            employee = Employee.objects.get(pk=id)
            form = EmployeeForm(request.POST,instance= employee)

            # print(employee.projects)


            # exit()
            dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30) 
            # current_time = datetime.datetime.now()
            employee.from_to = dt_India
            employee.save()

            return redirect('/employee/list')




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

def employee_list(request):
    print("-----------------u")
    context = {'employee_list': Employee.objects.all()}
    return render(request, "employee_register/employee_list.html", context)


def employee_delete(request,id):
    employee = Employee.objects.get(pk=id)
    employee.delete()
    return redirect('/employee/list')




    # Today Task 