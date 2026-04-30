from rest_framework import serializers
from .models import HomeVideo


class HomeVideoSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = HomeVideo
        fields = ["id", "video_url", "is_active", "updated_at"]

    def get_video_url(self, obj):
        url = obj.get_video_url()
        if url.startswith('/'):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(url)
            # Fallback if request is not in context
            return f"http://127.0.0.1:8000{url}"
        return url
