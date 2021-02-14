from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('user/CodeGenerator/', views.CodeGenerator, name="CodeGenerator"),
    path('user/SaveCircuit/<str:pk>/', views.SaveCircuit, name="SaveCircuit"),
    path('load_circuit/<str:pk>/', views.loadCircuit, name="load_circuit"),
    path('delete_circuit/<str:pk>/', views.deleteCircuit, name="delete_circuit"),
    path('help/', views.helpPage, name="help"),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),


]