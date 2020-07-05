from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('top', views.TopView.as_view(), name='top'),
]