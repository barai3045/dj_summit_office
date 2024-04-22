from django.shortcuts import get_object_or_404
from hr.models import Employee, EmployeeOffice, EmployeeTitle


def EmpTitle(eid, date):
    employee = get_object_or_404(Employee, pk=eid)
    title = employee.hire_title
    dt = employee.hire_date
    titles = EmployeeTitle.objects.all().filter(employee=eid).filter(date__lte=date)
    for x in titles:
        if dt < x.date:
            title = x.title
            dt = x.date
    return title


def EmpOffice(eid, date):
    employee = get_object_or_404(Employee, pk=eid)
    office = employee.hire_office
    dt = employee.hire_date
    offices = EmployeeOffice.objects.all().filter(employee = eid).filter(date__lte=date)

    for x in offices:
        if dt < x.date:
            office =x.office
            dt = x.date
    return office

