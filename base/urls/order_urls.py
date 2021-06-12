from django.urls import path
from base.views import order_views as views


#  this needs to be registered to the project bingolserver's urls.py
# note that routes ends with "/", not starting with


urlpatterns = [
    path("",views.getOrders, name="orders"),
    path('add/', views.addOrderItems, name='orders-add'),
    # this must be before <str:pk>/
    path('myorders/', views.getMyOrders, name='my-orders'),
    path('<str:pk>/deliver/', views.updateOrderToDelivered, name="order-deliver"),

    path('<str:pk>/', views.getOrderById, name='user-order'),
    path('<str:pk>/pay/', views.updateOrderToPaid, name='pay'),

    # path('users/register/', views.registerUser, name="register"),
    # path('products/', views.getProducts, name="products"),
    # path('users/profile/', views.getUserProfile, name="users-profile"),
    # path('users/', views.getUsers, name="users"),
    # path('products/<str:pk>',views.getProduct, name="product")
]