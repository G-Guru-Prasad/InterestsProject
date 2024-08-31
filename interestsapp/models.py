from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class InterestRecords(models.Model):
    interest_id = models.AutoField(primary_key=True)
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_id')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_id')
    status = models.CharField(max_length = 64)

class ChatMessages(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_chat_id')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_chat_id')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)