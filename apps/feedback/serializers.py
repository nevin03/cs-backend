from rest_framework import serializers
from .models import ClientFeedback


class ClientFeedbackSerializer(serializers.ModelSerializer):
    client_image_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientFeedback
        fields = [
            "id",
            "client_image_url",
            "client_name",
            "company_name",
            "description",
            "rating",
        ]

    def get_client_image_url(self, obj):
        request = self.context.get("request")
        if obj.client_image and request:
            return request.build_absolute_uri(obj.client_image.url)
        return obj.client_image.url if obj.client_image else None
