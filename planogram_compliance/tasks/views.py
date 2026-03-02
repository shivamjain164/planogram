from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from . import forms
import pandas as pd
from datetime import datetime, date
from . import filters
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# The function is to see the master tasks applicable for the country selected by the user on the country selection page. It also saves the country selected by the user in the session.
@login_required(login_url='login')
def task(request,pk):
    country = models.Country.objects.get(pk=pk)     
    task_applicable = models.MasterTasks.objects.filter(country=country)
    request.session["country"] = country.id
    return render(request,"tasks/home.html", context={"task_applicable": task_applicable})

# The below functions are to view the master data and add new entries in the master data tables like site, department, category and country. The master data is used while uploading the tasks through bulk upload or while adding/editing a task.

@login_required(login_url='login')
def master_data(request):
    return render(request, "tasks/master_data.html")

# The below functions are to view the master data of site
@login_required(login_url='login')
def site_data(request): 
    site = models.SiteData.objects.all()
    return render(request, template_name= "tasks/site_data.html", context={"site": site})

# The below function is to add new site in the site master data table.
@login_required(login_url='login')
def site_add(request):
    if request.method == "POST":
        form = forms.SiteDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("site_data")
    else:
        form = forms.SiteDataForm()
        return render(request, "tasks/site_add.html", {"form": form})
    
# The below functions are to view the master data of department 
@login_required(login_url='login')
def department(request):
    department = models.Department.objects.all()
    return render(request, "tasks/department.html", {"department": department})
    # return render(request, "tasks/department.html")
    
# The below function is to add new department in the department master data table. 
@login_required(login_url='login')   
def department_add(request):
    if request.method == "POST":
        form = forms.DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("department")
    else:
        form = forms.DepartmentForm()
        return render(request, "tasks/department_add.html", {"form": form})
@login_required(login_url='login')


# The below functions are to view the master data of category
def category(request):
    category = models.Category.objects.all()
    return render(request, "tasks/category.html", {"category": category})
    # return render(request, "tasks/category.html")
    
# The below function is to add new category in the category master data table.
@login_required(login_url='login')    
def category_add(request):
    if request.method == "POST":
        form = forms.CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("category")
    else:
        form = forms.CategoryForm()
        return render(request, "tasks/category_add.html", {"form": form})
    
    
# The below function is to view the list of countries in the country master data table. The user can also click on the country name to see the master tasks of the country.
@login_required(login_url='login')
def country_selection(request):
    country_data = models.Country.objects.all()
    return render(request, "tasks/country_selection.html", {"country_data": country_data})

# The below function is to add new country in the country master data table.
@login_required(login_url='login')
def country_add(request):
    if request.method == "POST":
        # form = forms.CountryForm()
        form = forms.CountryForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("country_selection")
    else:
        form = forms.CountryForm()
        return render(request, "tasks/country_add.html", {"form": form})
    
# The below function is to view the master tasks of a country. The user can click on the master task to see the individual tasks under that master task. 
@login_required(login_url='login')
def country(request):
    country_data = models.Country.objects.all()
    return render(request, "tasks/country.html", {"country_data": country_data})

# The below functions are to view the individual "in Progress" tasks under a master task. The tasks are filtered based on their status like not started, in progress, completed and cancelled. The user can also click on the planogram name to edit the task details.
@login_required(login_url='login')
def task_view_1(request,id):
    print(f"Task View 1 called with id: {id}")
    master_task = models.MasterTasks.objects.get(pk=id)
    status = models.Status.objects.all()
    task_data = models.Tasks.objects.filter(master_tasks = master_task, status = status[1])
    f = filters.TaskFilter(request.GET, queryset=models.Tasks.objects.filter(master_tasks = master_task))
    return render(request, "tasks/in_progress.html", {"task_data": task_data, "task":id, "filter": f})
@login_required(login_url='login')

# The below functions are to view the individual "Not Started" tasks under a master task. The tasks are filtered based on their status like not started, in progress, completed and cancelled. The user can also click on the planogram name to edit the task details.

def task_view_0(request,id):
    master_task = models.MasterTasks.objects.get(pk=id)
    status = models.Status.objects.all()
    task_data = models.Tasks.objects.filter(master_tasks = master_task, status = status[0])
    return render(request, "tasks/not_started.html", {"task_data": task_data, "task":id})
@login_required(login_url='login')

# The below functions are to view the individual "Completed" tasks under a master task. The tasks are filtered based on their status like not started, in progress, completed and cancelled. The user can also click on the planogram name to edit the task details.

def task_view_2(request,id):
    master_task = models.MasterTasks.objects.get(pk=id)
    status = models.Status.objects.all()
    task_data = models.Tasks.objects.filter(master_tasks = master_task, status = status[2])
    return render(request, "tasks/completed.html", {"task_data": task_data, "task":id})

# The below functions are to view the individual "Cancelled" tasks under a master task. The tasks are filtered based on their status like not started, in progress, completed and cancelled. The user can also click on the planogram name to edit the task details.

@login_required(login_url='login')
def task_view_3(request,id):
    master_task = models.MasterTasks.objects.get(pk=id)
    status = models.Status.objects.all()
    task_data = models.Tasks.objects.filter(master_tasks = master_task, status = status[3])
    return render(request, "tasks/cancelled.html", {"task_data": task_data, "task":id})

# The below function is to handle the bulk upload of tasks through a csv file. The function checks if the uploaded file has the expected columns and if the data in the columns is valid based on the master data tables. If there are any issues with the uploaded file, it returns an error message. If the file is valid, it saves the master task and individual tasks in the database and redirects to the in progress task view of the uploaded master task.
@login_required(login_url='login')  
def bulk_upload(request):
    if request.method == "POST":
        form = forms.BulkUploadForm(request.POST, request.FILES)
        uploaded_file = request.FILES["uploaded_file"]
        deadline = request.POST.get("deadline")
        if datetime.strptime(deadline, "%Y-%m-%d").date() < date.today():
            return HttpResponse("Deadline is in the past. Please enter a valid deadline.")
        title = request.POST.get("title")

        df = pd.read_csv(uploaded_file)

        actual_columns = df.columns.tolist()
        expected_columns = ['Store Number',"Store Name", 'Department Name', 'Category Name', 'Planogram Name', 'Bays Required', "Start Date", 'Deadline', 'Description']
        if actual_columns != expected_columns:
            return HttpResponse("Invalid file, the columns do not match the expected format.")
        store_number = df["Store Number"].to_list()
        department_name = df["Department Name"].tolist()
        category_name = df["Category Name"].tolist()
        store_number_db = models.SiteData.objects.filter(country = request.session.get("country"))
        department_db = models.Department.objects.filter(country = request.session.get("country"))
        category_db = models.Category.objects.filter(department__country = request.session.get("country"))

        for i in store_number:
            if str(i) not in store_number_db.values_list("site_id", flat=True):
                return HttpResponse(f"Store Number {i} does not exist in the database.")
        
        for i in department_name:
            if str(i) not in str(department_db.values_list("department_code", flat=True)):
                return HttpResponse(f"Department Name {i} does not exist in the database.")
        
        for i in category_name:
            if str(i) not in str(category_db.values_list("category_code", flat=True)):
                return HttpResponse(f"Category Name {i} does not exist in the database.")
        # Check deadline format 
        df_startdate = df["Start Date"].tolist()
        for i in df_startdate:
            today_date = date.today()
            start_date = datetime.strptime(i, "%d-%m-%Y").date()
            if start_date < today_date:
                return HttpResponse(f"Start Date {i} is in the past. Please enter a valid start date.")
            
        df_deadline = df["Deadline"].tolist()
        for i in df_deadline:
            today_date = date.today()
            deadline = datetime.strptime(i, "%d-%m-%Y").date()
            if deadline < today_date:
                return HttpResponse(f"Deadline {i} is in the past. Please enter a valid deadline.")
        
        # Saving data in master Tasks
        chac_title_master_task = models.MasterTasks.objects.filter(title = request.POST.get("title"))
        if chac_title_master_task.exists():
            return HttpResponse("Master Task with this title already exists. Please change the title and try again.")
        master_task = models.MasterTasks.objects.create(
            country = models.Country.objects.get(pk = request.session.get("country")),
            title = title,
            deadline = deadline,
        )
        master_task.save()

        saved_master_task = models.MasterTasks.objects.get(title = title)
        # Save individual tasks
        for index, row in df.iterrows():
            site_instance = models.SiteData.objects.get(site_id = row["Store Number"], country = request.session.get("country"))
            department_instance = models.Department.objects.get(department_code = row["Department Name"], country = request.session.get("country"))
            category_instance = models.Category.objects.get(category_code = row["Category Name"], department__country = request.session.get("country"))
            
            deadline = pd.to_datetime(row["Deadline"], format = "%d-%m-%Y")
            if deadline.date() == date.today():
                status_instance = models.Status.objects.get(status = "In Progress")
            
            else:
                status_instance = models.Status.objects.get(status = "Not Started")
            task_instance = models.Tasks.objects.create(
                site = site_instance,
                department = department_instance,
                category = category_instance,
                master_tasks = saved_master_task,
                status = status_instance,
                planogram = row["Planogram Name"],
                bays = row["Bays Required"],
                task_description = row["Description"],
                deadline = deadline,
            
                user = models.User.objects.first(), # Replace with actual user instance as needed
            )
            task_instance.save()
        f = filters.TaskFilter(request.GET, queryset=models.Tasks.objects.filter(master_tasks = saved_master_task))
        return redirect("task_view_1", id = saved_master_task.id)
    else:
        form = forms.BulkUploadForm()
        return render(request, "tasks/bulk_upload.html", {"form": form})
    
@login_required(login_url='login')    
# The below function is to edit the task details when the user clicks on the planogram name in the task view page. The user can edit the task details and save the changes. After saving, the user is redirected to the in progress task view of the master task to which the edited task belongs.
def taskedit(request, id):
    task_instance = models.Tasks.objects.get(pk=id)
    print(task_instance.id)
    if request.method == "POST":
        form = forms.TaskForm(request.POST, instance=task_instance)
        if form.is_valid():
            form.save()
            master_task_id = task_instance.master_tasks.id
            print(form)
            return redirect("task_view_1", id=master_task_id)
    else:
        form = forms.TaskForm(instance=task_instance)
        return render(request, "tasks/task_edit.html", {"form": form, "task_id": id})
    
    # The below function is to handle the login of the user. The user enters the username and password and if the credentials are valid, the user is logged in and redirected to the country selection page. If the credentials are invalid, an error message is displayed.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('country_selection')
        else:
            messages.error(request, 'Invalid credentials')
    form = forms.LoginForm()
    return render(request, 'tasks/login.html', {'form': form})
    # return render(request, 'tasks/login.html')