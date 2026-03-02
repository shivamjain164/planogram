from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('task/<int:pk>/', views.task, name='task'),
    path("master_data", views.master_data, name = "master_data"),
    path("site_data", views.site_data, name = "site_data"),
    path("department", views.department, name = "department"),
    path("category", views.category, name = "category"),
    path("country_selection", views.country_selection, name = "country_selection"),
    path("country_add", views.country_add, name = "country_add"),
    path("site_add", views.site_add, name = "site_add"),
    path("department_add", views.department_add, name = "department_add"),
    path("category_add", views.category_add, name = "category_add"),
    # path("master_tasks", views.master_tasks, name = "master_tasks"),
    path("country", views.country, name = "country"),
    path("task_view_1/<int:id>", views.task_view_1, name = "task_view_1"),
    path("task_view_0/<int:id>", views.task_view_0, name = "task_view_0"),
    path("task_view_2/<int:id>", views.task_view_2, name = "task_view_2"),
    path("task_view_3/<int:id>", views.task_view_3, name = "task_view_3"),
    path("bulk_upload", views.bulk_upload, name = "bulk_upload"),
    path("task_edit/<int:id>", views.taskedit, name = "task_edit"),
    path("login", views.login_view, name='login'),
]