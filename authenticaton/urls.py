from django.urls import path
from authenticaton.views import *
from authenticaton import views

urlpatterns = [
    path('', SignUpView.as_view(),name="signup"),
    path('login', LoginView.as_view(),name="login"),
    path('<pk>/', UserDetailView.as_view(),name="UserDetailView"),
    path('update/<pk>', UserUpdate.as_view(),name="UserUpdateView"),
    path('userslist', UserList.as_view(),name="userslist"),
    path('logout', views.logout_view,name="logout"),

]
