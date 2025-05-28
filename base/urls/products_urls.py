from django.urls import path
from base.views import products_views as views

urlpatterns = [
    path('', views.getProducts, name="products"),
    path('<int:pk>/', views.getProduct, name="product"),
    path('<int:pk>/review/', views.createProductReview, name="create-product-review"),
    path('create/', views.createProduct, name="create-product"),
    path('upload/', views.uploadImage, name="upload-image"),
    path('delete/<int:pk>/', views.deleteProduct, name="delete-product"),
    path('update/<int:pk>/', views.updateProduct, name="update-product"),
    path('top/', views.topProducts, name="top-products")
]