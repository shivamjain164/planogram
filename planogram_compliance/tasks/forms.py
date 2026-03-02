from django import forms
from . import models

class CountryForm(forms.ModelForm):
    class Meta:
        model = models.Country
        fields = '__all__'        
class SiteDataForm(forms.ModelForm):
    class Meta:
        model = models.SiteData
        fields = '__all__'
        
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = models.Department
        fields = '__all__'
        
class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = models.Category
        fields = '__all__'
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Tasks
        fields = '__all__'
        
class MasterTasksForm(forms.ModelForm):
    class Meta:
        model = models.MasterTasks
        fields = '__all__'
        
class BulkUploadForm(forms.ModelForm):
    class Meta:
        model = models.BulkUpload
        fields = '__all__'
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'step': '60'}), # Add 'step':'60' if you want to allow minutes selection
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)