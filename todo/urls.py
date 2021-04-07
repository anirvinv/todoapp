from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.log_out, name="logout"),
    path('login/', views.log_in, name="login"),
    path('register/', views.sign_up, name="signup"),
    path('add/', views.add, name="add")
]