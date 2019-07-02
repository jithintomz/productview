from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("products/",
         views.ProductViewSet.as_view({'get': 'list'}), name="products"),
    path("products/<int:pk>", views.ProductViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete':'destroy'}), name="product-details"),
    path("upload-products/", views.ProductsUploadView.as_view(),
         name="upload-products")
]
