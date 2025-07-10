from django.urls import path
from myapp.modules.login.views import views

urlpatterns = [
    path('api/login',views.login),
    path('api/register',views.register),
    path('api/logout',views.logout),
]