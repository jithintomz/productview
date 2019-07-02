from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django_eventstream import send_event

from acme.settings import REST_FRAMEWORK as rest_settings
from productview import utils
from productview import tasks
from productview.serializers import ProductSerializer
from productview.models import Product,Upload

def index(request):
	response = render(request,'index.html')
	return response


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("name")
    def get_queryset(self):
        if "keyword" in self.request.query_params:
            self.queryset = self.queryset.filter(name__icontains=self.request.query_params["keyword"])
        return self.queryset





class ProductsUploadView(APIView):
    """View responsible for processing products
    csv uploaded by user"""

    def post(self, request):
        products_csv = request.FILES["file"]
        upload_id = utils.save_csv(products_csv)
        return Response({"upload_id": upload_id})

    def get(self, request):
        """Gets the latest upload for simple stuff"""
        
        upload = Upload.objects.filter().values().last()
        return Response(upload)
