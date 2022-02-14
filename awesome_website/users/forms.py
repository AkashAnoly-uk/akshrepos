from django import forms
# from .models import Employee
# from .widgets import DateTimePickerInput
# from django.forms import ModelForm
from .models import projects
from .models import employee_details


# class DateInput(forms.DateInput):
#     input_type = 'date'


# class EmployeeForm(forms.ModelForm):

#     class Meta:
#         model = Employee
#         # fields = fields = "__all__"
#         fields = ['full_name', 'mobile', 'projects','platform']
#         # widgets = {
            
#         #     'from_to': DateInput(),
        # }

        
       
class ProjForm(forms.ModelForm):
    class Meta:
        model = projects
        fields = ['project_name', 'platform_name']





class CheckForm(forms.ModelForm):
    class Meta:
        model = employee_details
        fields = ['mobile']


        
        
