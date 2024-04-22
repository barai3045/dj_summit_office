from django.urls import path
from management.approval import views

app_name = "approval"

urlpatterns = [
    path('', views.approval_home, name="approval_home"),
    path('<int:pk>', views.approval_view, name="approval_view"),
    path('report/<int:pk>', views.approval_report, name="approval_report"),
    
    path('quotaiton/', views.quotation_home, name="quotation_home"),
    path('quotaiton/<str:pk>', views.quotation_view, name="quotation_view"),
    
    path('title/', views.title_home, name="title_home"),
    path('title/<int:pk>', views.title_view, name="title_view"),
]