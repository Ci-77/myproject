from django.urls import path
from myapp.modules.login.views import views

urlpatterns = [
    path('login',views.login),
    path('register',views.register),
    path('logout',views.logout),
]