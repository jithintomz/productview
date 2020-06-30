"""This file acts at the starting point for all application
logic of rest end-points"""

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Q
from django.db import IntegrityError

from productview import utils
from productview.serializers import (
    ProductSerializer, WebhookSerializer, EventSerializer
)
from productview.models import Product, Upload, WebHook, Event


def index(request):
    response = render(request, 'index.html')
    return response


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("name")

    def get_queryset(self):
        if "keyword" in self.request.query_params:
            self.queryset = self.queryset.filter(
                Q(name__icontains=self.request.query_params["keyword"]) |
                Q(sku__icontains=self.request.query_params["keyword"]))
        if "filter" in self.request.query_params:
            filter_array = self.request.query_params["filter"].split(",")
            filter_array = list(map(int, filter_array))
            self.queryset = self.queryset.filter(is_active__in=filter_array)
        return self.queryset

    def create(self, request):
        """Creates product instance"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["sku"] = \
                serializer.validated_data["sku"].lower()
            try:
                product = serializer.save()
            except IntegrityError:
                Product.objects.get(
                    sku=serializer.validated_data["sku"]
                ).delete()
                product = serializer.save()
            utils.notify_hooks("create_product", product)
            return Response(status=204)
        else:
            return Response(serializer.errors, status=400)

    def update(self, request, pk):
        """Updates the product instance based on pk"""

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            prod_object = Product.objects.get(pk=pk)
            serializer.validated_data["sku"] = \
                serializer.validated_data["sku"].lower()
            try:
                product = serializer.update(
                    prod_object, serializer.validated_data
                )
            except IntegrityError:
                Product.objects.get(
                    sku=serializer.validated_data["sku"].delete()
                )
                product = serializer.update(
                    prod_object, serializer.validated_data
                )
            utils.notify_hooks("update_product", product)
            return Response(status=204)
        else:
            return Response(serializer.errors, status=400)


class HookViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing webhooks.
    """
    serializer_class = WebhookSerializer
    queryset = WebHook.objects.all().order_by("name")


class EventViewSet(viewsets.ModelViewSet):
    """
        viewset for listing Events
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by("name")


class ProductsUploadView(APIView):

    """View responsible for processing products
    csv uploaded by user"""

    def post(self, request):
        products_csv = request.FILES["file"]
        upload_id = utils.save_csv(products_csv)
        return Response({"upload_id": upload_id})

    def get(self, request):
        """Gets the latest upload in progress for tracking"""
        upload = Upload.objects.filter().values().last()
        return Response(upload)
