from django.urls import path

from admin.views import get_all_order, delete_order, assign_order_courier
from authentication.views import sign_up ,user_login ,user_logout

urlpatterns = [
    path('orders', get_all_order),
    path('order/delete/<str:variable>', delete_order),
    path('order/courier', assign_order_courier)
]