from rest_framework import serializers
from .models import PricingPackage, PricingFeature


class PricingFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingFeature
        fields = ["id", "feature_text", "is_included", "order"]


class PricingPackageSerializer(serializers.ModelSerializer):
    features = PricingFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = PricingPackage
        fields = [
            "id",
            "package_name",
            "price",
            "price_label",
            "is_featured",
            "features",
        ]
