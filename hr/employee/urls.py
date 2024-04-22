from django.urls import path

from hr.employee import views


app_name = "employee"

urlpatterns = [
    path('employee/', views.emplyee_home, name="employee_home"),
    path('employee/<str:pk>', views.employee_view, name="employee_view"),
    path('office/', views.office_home, name="office_home"),
    path('office/<int:pk>', views.office_view, name="office_view"),
    path('title/', views.title_home, name="title_home"),
    path('title/<int:pk>', views.title_view, name="title_view"),
   
]