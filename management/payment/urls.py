from django.urls import path
from management.payment import views

app_name = "payment"

urlpatterns = [
    path('invoice/home', views.invoice_home, name="invoice_home"),
    path('invoice/view/<int:pk>', views.invoice_view, name="invoice_view"),
    path('invoice/report/<int:pk>', views.invoice_report, name="invoice_report"),
    path('others/home', views.others_home, name="others_home"),
    path('others/view/<int:pk>', views.others_view, name="others_view"),
    path('others/report/<int:pk>', views.others_report, name="others_report"),
]