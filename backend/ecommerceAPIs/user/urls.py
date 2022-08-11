from django.urls import path
from .views import CreateUserView, CreateTokenView, ManageUserView,AdminUsersAPIs, UserAPIs

urlpatterns = [
    path("registeruser/", CreateUserView.as_view(), name="registeruser"),
    path("generatetoken/", CreateTokenView.as_view(), name="generatetoken"),
    path("manageuser/", ManageUserView.as_view(), name="manageuser"),
    
    path("adminuserlist/", AdminUsersAPIs.as_view(), name="users"),
    path("userdetailsbyadmin/<int:pk>", AdminUsersAPIs.as_view(), name="userbyid"),
    
    path("userdetailsbyuser/<int:pk>", UserAPIs.as_view(), name="userdetails"),
    path("profile/", UserAPIs.as_view(), name="userdetailsbbyuser"),
]
