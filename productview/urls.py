"""All urls corresponding to productview app"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
         "events/",
         views.EventViewSet.as_view({'get': 'list'}),
         name="events"
     ),
    path(
         "products/",
         views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}),
         name="products"
     ),
    path(
         "products/<int:pk>",
         views.ProductViewSet.as_view({
              'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
          }),
     ),
    path(
         "hooks/",
         views.HookViewSet.as_view({'get': 'list', 'post': 'create'}),
         name="web-hooks"
     ),
    path(
         "hooks/<int:pk>",
         views.HookViewSet.as_view({
              'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
          ),
    path(
         "upload-products/",
         views.ProductsUploadView.as_view(),
         name="upload-products"
     )
]
