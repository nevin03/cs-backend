import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import ChatSession
from .serializers import ChatMessageSerializer
from .services.chat_flow import handle_chat

logger = logging.getLogger(__name__)

class ChatAPIView(APIView):
    @extend_schema(
        tags=["Chatbot"],
        request=ChatMessageSerializer,
        responses={200: dict},
        summary="Handle chatbot interactions",
        description="Progresses through the chat flow based on session_id and user message.",
        examples=[
            OpenApiExample(
                "Start Session",
                value={"session_id": "abc123", "message": ""},
                request_only=True,
            )
        ]
    )
    def post(self, request):
        serializer = ChatMessageSerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data['session_id']
            message = serializer.validated_data.get('message', '')
            
            extra_data = {
                "name": serializer.validated_data.get("name", ""),
                "location": serializer.validated_data.get("location", ""),
                "contact": serializer.validated_data.get("contact", ""),
                "services": serializer.validated_data.get("services", ""),
            }

            # Retrieve or create the session
            session, created = ChatSession.objects.get_or_create(session_id=session_id)
            if created:
                logger.info(f"New chat session created: {session_id}")

            try:
                response_data = handle_chat(session, message, extra_data)
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error handling chat for session {session_id}: {str(e)}")
                return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
