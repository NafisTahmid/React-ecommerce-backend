from django.urls import path
from base.views import orders_views as views

urlpatterns = [
    path('', views.getOrders, name="orders"),
    path('add/', views.addOrderItems, name="orders-add"),
    path('myorders/', views.getMyOrders, name="myorders"),
    path('<int:pk>/deliver/', views.updateOrderToDelivered, name="deliver-order"),
    path('<int:pk>/', views.getOrderById, name="user-order"),
    path('<int:pk>/pay/', views.updateOrderToPaid, name="pay"),
]