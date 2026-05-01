from rest_framework import serializers

class ChatMessageSerializer(serializers.Serializer):
    session_id = serializers.CharField(required=True)
    message = serializers.CharField(allow_blank=True, required=False, default="")
    # Support for frontend sending all data at once
    name = serializers.CharField(allow_blank=True, required=False, default="")
    location = serializers.CharField(allow_blank=True, required=False, default="")
    contact = serializers.CharField(allow_blank=True, required=False, default="")
    services = serializers.CharField(allow_blank=True, required=False, default="")
