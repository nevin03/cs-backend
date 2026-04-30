from rest_framework import serializers
from .models import ContactSubmission


class ContactSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for incoming POST data. ip_address is set by the view."""

    class Meta:
        model = ContactSubmission
        fields = ["id", "name", "email", "project_enquiry", "submitted_at"]
        read_only_fields = ["id", "submitted_at"]

    def validate_email(self, value):
        return value.lower().strip()

    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters.")
        return value

    def validate_project_enquiry(self, value):
        value = value.strip()
        if len(value) < 20:
            raise serializers.ValidationError(
                "Please describe your project in at least 20 characters."
            )
        return value
