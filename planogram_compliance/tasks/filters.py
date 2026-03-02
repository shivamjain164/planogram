import django_filters
from . import models

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = models.Tasks
        fields = ['site', 'department', 'category', 'status', "planogram", "deadline", "user"]