from django.urls import path

from order.views import create_order, get_all_order, get_order, update_order, get_order_courier

urlpatterns = [
    path('add', create_order),
    path('list', get_all_order),
    path('get/<str:variable>', get_order),
    path('update/<str:variable>', update_order),
    path('courier/<str:variable>', get_order_courier)
]