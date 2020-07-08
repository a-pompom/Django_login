from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    # ログイン
    path('', views.LoginView.as_view(), name='login'),
    # ユーザ登録
    path('signup', views.SignUpView.as_view(), name='signup'),
    # トップ
    path('top', views.TopView.as_view(), name='top'),
    # ログアウト
    path('logout', views.LogoutView.as_view(), name='logout'),
]