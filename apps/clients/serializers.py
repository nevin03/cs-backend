from rest_framework import serializers
from .models import ClientLogo


class ClientLogoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ClientLogo
        fields = ["id", "image", "alt_text"]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.logo and request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url if obj.logo else None
