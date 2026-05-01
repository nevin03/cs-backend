from rest_framework import serializers
from .models import FeaturedProject, ProjectImage, ProjectLink, ProjectTag


class ProjectTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTag
        fields = ["id", "name"]


class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = ["id", "label", "url", "order"]


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
    tags = ProjectTagSerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)
    links = ProjectLinkSerializer(many=True, read_only=True)
    video = serializers.SerializerMethodField()
    project_image_item = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedProject
        fields = [
            "id",
            "title",
            "tags",
            "project_name",
            "slug",
            "description",
            "project_image_item",
            "industry",
            "links",
            "images",
            "video",
            "banner_video",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "order",
            "created_at",
        ]

    def get_video(self, obj):
        if obj.banner_video:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.banner_video.url)
            return obj.banner_video.url
        return None

    def get_project_image_item(self, obj):
        if obj.project_image_item:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.project_image_item.url)
            return obj.project_image_item.url
        return None


class FeaturedProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views — omits SEO fields."""

    tags = ProjectTagSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()
    project_image_item = serializers.SerializerMethodField()
    links = ProjectLinkSerializer(many=True, read_only=True)

    class Meta:
        model = FeaturedProject
        fields = [
            "id",
            "title",
            "tags",
            "project_name",
            "slug",
            "description",
            "thumbnail",
            "video",
            "project_image_item",
            "industry",
            "links",
            "banner_video",
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
        if obj.banner_video:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.banner_video.url)
            return obj.banner_video.url
        return None

    def get_project_image_item(self, obj):
        if obj.project_image_item:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.project_image_item.url)
            return obj.project_image_item.url
        return None
