from django.urls import path
from .views import  ProductAPIS

urlpatterns = [
    
    path("product/", ProductAPIS.as_view(), name="product"),
    path("product/<int:pk>", ProductAPIS.as_view(), name="productbyid"),
]
