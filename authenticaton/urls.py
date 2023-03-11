from django.urls import path
from authenticaton.views import *

urlpatterns = [
    path('', SignUpView.as_view(),name="signup"),
    path('login', LoginView.as_view(),name="login"),
    path('<pk>/', UserDetailView.as_view(),name="UserDetailView"),
    path('update/<pk>', UserUpdate.as_view(),name="UserDetailView"),
    path('userslist', UserList.as_view(),name="userslist"),

]
