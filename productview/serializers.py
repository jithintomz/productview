from rest_framework import serializers

from productview.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "description",
                  "upload_id", "created_time", "updated_time")
