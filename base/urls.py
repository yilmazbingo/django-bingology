# from django.urls import path
# from . import views
#
#
# #  this needs to be registered to the project bingolserver's urls.py
# # note that routes ends with "/", not starting with
#
#
# urlpatterns=[
#     path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('users/register/', views.registerUser, name="register"),
#     path('products/', views.getProducts, name="products"),
#     path('users/profile/', views.getUserProfile, name="users-profile"),
#     path('users/', views.getUsers, name="users"),
#     path('products/<str:pk>',views.getProduct, name="product")
# ]