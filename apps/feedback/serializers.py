from rest_framework import serializers
from .models import ClientFeedback


class ClientFeedbackSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ClientFeedback
        fields = [
            "id",
            "image_url",
            "client_name",
            "company_name",
            "description",
            "rating",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None
