from django.urls import path
from . import views

urlpatterns = [
    path('', views.accounts_navbar_view, name='accounts_navbar'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_edit/', views.profile_edit_view, name='profile_edit'),
    path('change_password/', views.change_password_view, name='change_password'),
    path('delete_account/', views.delete_account_view, name='delete_account'),
    path('password_forget/', views.password_forget_view, name='password_forget'),
]
