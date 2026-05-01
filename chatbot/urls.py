from django.urls import path
from .views import ChatAPIView

app_name = "chatbot"

urlpatterns = [
    path("", ChatAPIView.as_view(), name="chat"),
]
