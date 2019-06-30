from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload-products/", views.ProductsUploadView.as_view(),
         name="upload-products")
]
