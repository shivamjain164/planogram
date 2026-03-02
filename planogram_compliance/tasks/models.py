from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.name} '
    
    
class SiteData(models.Model):    
    country = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='site_data')
    site_name = models.CharField(max_length = 50)
    site_id = models.CharField(max_length = 6)
    
    def __str__(self):
        return f"  {self.site_name} - {self.site_id}"
    
    
class Department(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='department')
    department_code = models.IntegerField()
    department_name = models.CharField(max_length = 30)
    
    def __str__(self):
        return f" {self.department_name} - {self.department_code}"
    
class Category(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='category')
    category_code = models.IntegerField()
    category_name = models.CharField(max_length = 30)
    
    def __str__(self):
        return f" {self.category_code} - {self.category_name}"
    

class MasterTasks(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='master_tasks_country')
    title = models.CharField(max_length = 30)
    modified_time  = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField() 

    def __str__(self):
        return f" {self.title} - {self.modified_time} - {self.deadline}"
    
class Status(models.Model):
    status = models.CharField(max_length = 20)
    
    def __str__(self):
        return f" {self.status}"
    
    
class Tasks(models.Model):
    # country = models.ForeignKey(Country,on_delete=models.CASCADE, related_name='country_info')
    site = models.ForeignKey(SiteData,on_delete=models.CASCADE, related_name='site_info')
    department = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='department_info')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='category_info')
    master_tasks = models.ForeignKey(MasterTasks,on_delete=models.CASCADE, related_name='master_tasks_info', default=1)
    status = models.ForeignKey(Status,on_delete=models.CASCADE, related_name='status_info')
    planogram = models.CharField(max_length = 250)
    bays = models.IntegerField()
    task_description = models.CharField(max_length = 250, null = True, blank = True)
    start_time = models.DateTimeField(blank=True, null=True)
    modified_time  = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_info')
    retaier_selected_planogram = models.CharField(max_length = 250, null = True, blank = True)
    
    def __str__(self):
        return f" Task Name is {self.planogram} with description as {self.task_description}"
    
class BulkUpload(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 30, blank=True, null=True)
    deadline  = models.DateTimeField(blank=True, null=True)