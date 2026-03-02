from django.contrib import admin
from . import models
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(models.Country)
admin.site.register(models.SiteData)
admin.site.register(models.Department)
admin.site.register(models.Category)
admin.site.register(models.Tasks)
admin.site.register(models.MasterTasks)
admin.site.register(models.Status)
admin.site.register(models.BulkUpload)
# admin.site.register(User)