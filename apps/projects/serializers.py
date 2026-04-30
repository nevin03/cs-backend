from rest_framework import serializers
from .models import FeaturedProject, ProjectImage


class ProjectImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProjectImage
        fields = ["id", "image_url", "alt_text", "order"]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url if obj.image else None


class FeaturedProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    video = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedProject
        fields = [
            "id",
            "title",
            "tag",
            "project_name",
            "slug",
            "description",
            "images",
            "video",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "order",
            "created_at",
        ]

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.project_video and request:
            return request.build_absolute_uri(obj.project_video.url)
        return obj.project_video_url or None


class FeaturedProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — omits SEO fields."""

    thumbnail = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedProject
        fields = [
            "id",
            "title",
            "tag",
            "project_name",
            "slug",
            "description",
            "thumbnail",
            "video",
        ]

    def get_thumbnail(self, obj):
        first_image = obj.images.first()
        if not first_image:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(first_image.image.url)
        return first_image.image.url

    def get_video(self, obj):
        request = self.context.get("request")
        if obj.project_video and request:
            return request.build_absolute_uri(obj.project_video.url)
        return obj.project_video_url or None
