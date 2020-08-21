from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('pizza/', views.PizzaList.as_view(), name='pizza_list'),
    path('pizza/<int:pk>/', views.PizzaDetail.as_view(), name='pizza_detail'),

    path('order/', views.OrderList.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OrderDetail.as_view(), name='order_detail'),
]
