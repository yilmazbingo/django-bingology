from django.urls import path
from base.views import product_views as views


#  this needs to be registered to the project bingolserver's urls.py
# note that routes ends with "/", not starting with


urlpatterns=[
    path('', views.getProducts, name="products"),
    path('create/', views.createProduct, name="product-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path("upload-image/", views.upload, name="upload-image"),
    path('<str:pk>/reviews/', views.createProductReview, name="create-review"),
    path('top/',views.getTopProducts, name='top-products'),
    # <str:pk> tells django pk should be converted to string
    path('<str:pk>/', views.getProduct, name="product"),
    path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),
    path('update/<str:pk>/', views.updateProduct, name="update-product")
]