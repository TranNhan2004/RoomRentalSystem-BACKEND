from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Conversation, Message
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class ConversationSerializer(ModelSerializer):
    user_1 = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    user_2 = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Conversation
        fields = '__all__'


# -----------------------------------------------------------
class MessageSerializer(ModelSerializer):
    conversation = PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    sender = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    
    class Meta:
        model = Message
        fields = '__all__'