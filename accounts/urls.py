from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_order/', views.create_order, name='create_order'),
    path('create_customer/', views.create_customer, name="create_customer"),
    path('update_order/<str:pk>/', views.update_order, name="update_order"),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),
    path('update_customer/<str:pk>/', views.update_customer, name='update_customer'),
    path('delete_customer/<str:pk>/', views.delete_customer, name='delete_customer'),
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='userPage'),
    path('account/', views.accountSettings, name='account'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
