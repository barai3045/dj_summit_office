from django.urls import path
from management.order import views

app_name = "order"

urlpatterns = [
    path('', views.order_home, name="order_home"),
    path('<int:pk>', views.order_view, name="order_view"),
    path('report/<int:pk>', views.order_report, name="order_report"),
]