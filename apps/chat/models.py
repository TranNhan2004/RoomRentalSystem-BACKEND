import uuid

from django.db import models
from apps.user_account.models import CustomUser


# -----------------------------------------------------------
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user_1 = models.ForeignKey(CustomUser, related_name='coversations_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(CustomUser, related_name='coversations_user_2', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
        
# -----------------------------------------------------------
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=2048)
    
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sent_by = models.ForeignKey(CustomUser, related_name='sent_messages', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)