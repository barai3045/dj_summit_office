from django.urls import path
from management.base import views
app_name = "management_base"

urlpatterns = [
    path('vendor/home', views.vendor_home, name="vendor_home"),
    path('vendor/view/<int:pk>', views.vendor_view, name="vendor_view"),
]