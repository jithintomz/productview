from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django_eventstream import send_event

from productview import utils
from productview import tasks

def index(request):
    
    tasks.sender.delay()
    return HttpResponse("success")

class ProductsUploadView(APIView):
    """View responsible for processing products
    csv uploaded by user"""

    def put(self, request):
        products_csv = request.FILES["file"]
        utils.save_csv(products_csv)
        return Response(status = 204)
