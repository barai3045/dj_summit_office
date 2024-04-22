import datetime
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from hr.funs import EmpTitle, EmpOffice


from hr.models import Employee, EmployeeOffice, EmployeeTitle, Office, Title


def emplyee_home(request):
    template_path = "hr/employee/home.html"

    employees = Employee.objects.all()
    paginator = Paginator(employees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
    'xs': page_obj
    }
    return render(request, template_path, context)


def employee_view(request, pk):
    template_path = "hr/employee/view.html"
    employee = get_object_or_404(Employee, pk=pk)
    employee.titles = EmployeeTitle.objects.all().filter(employee=employee)
    employee.offices = EmployeeOffice.objects.all().filter(employee=employee)

    context = {
        'x': employee

    }

    return render(request, template_path, context)


def office_home(request):
    template_path = "hr/office/home.html"
    offices  = Office.objects.all().order_by('id')
    paginator = Paginator(offices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'xs': page_obj,
    }
    return render(request, template_path, context)


def office_view(request, pk):
    template_path = "hr/office/view.html"

    office = get_object_or_404(Office, pk=pk)

    context = {
        'x': office,
    }

    return render(request, template_path, context)


def title_home(request):
    template_path = "hr/title/home.html"
    titles = Title.objects.all().order_by('id')
    paginator = Paginator(titles, 10 )
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'xs': page_obj,
    }

    return render(request, template_path, context)


def title_view(request, pk):
    template_path = "hr/title/view.html"
    title = get_object_or_404(Title, pk=pk)
    context = {
        'x': title,
    }

    return render(request, template_path, context)
