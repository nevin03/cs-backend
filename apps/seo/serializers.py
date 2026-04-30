from rest_framework import serializers
from .models import SEOPage


class SEOPageSerializer(serializers.ModelSerializer):
    og_image_url = serializers.SerializerMethodField()

    class Meta:
        model = SEOPage
        fields = [
            "page",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "og_title",
            "og_description",
            "og_image_url",
            "canonical_url",
            "updated_at",
        ]

    def get_og_image_url(self, obj):
        request = self.context.get("request")
        if obj.og_image and request:
            return request.build_absolute_uri(obj.og_image.url)
        return obj.og_image.url if obj.og_image else None
