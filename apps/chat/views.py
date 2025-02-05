from rest_framework import viewsets

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


# -----------------------------------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer


# -----------------------------------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer