from django.urls import path
from .views import  UserOrdersAPIs, AdminOrdersAPIs, OrderItemsAPIs

urlpatterns = [
    
    path("userorders/", UserOrdersAPIs.as_view(), name="userorders"),
    path("userorders/<int:pk>", UserOrdersAPIs.as_view(), name="userorderbyid"),
    path("orderlist/", AdminOrdersAPIs.as_view(), name="orderlist"),
    path("orderitems/", OrderItemsAPIs.as_view(), name="orderitems"),
]