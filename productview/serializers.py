from rest_framework import serializers

from productview.models import Product, WebHook, Event


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "sku", "description", "is_active",
                  "upload_id", "created_time", "updated_time")
        extra_kwargs = {
            'sku': {
                'validators': [],
            },
        }


class WebhookSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source="event.name")

    class Meta:
        model = WebHook
        fields = ("id", "name", "url", "event", "event_name", "updated_time")


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ("id", "name", "code")
