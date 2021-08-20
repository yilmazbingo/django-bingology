from django.urls import path
from base.views import user_views as views


#  this needs to be registered to the project bingolserver's urls.py
# note that routes ends with "/", not starting with


urlpatterns=[
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', views.registerUser, name="register"),
    path('profile/', views.getUserProfile, name="users-profile"),
    path('update/<str:pk>/', views.updateUser, name="user-update"),
    path('profile/update/', views.updateUserProfile, name="users-profile-update"),
    path('<str:pk>/', views.getUserById, name='user'),
    path('delete/<str:pk>/', views.deleteUser, name="user-delete"),
    path('update/', views.getUserById, name="user"),

    path('', views.getUsers, name="users"),
]