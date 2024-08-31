from rest_framework import serializers
from .models import InterestRecords, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class InterestRecordsSerializer(serializers.ModelSerializer):
    sender_id = UserSerializer()
    receiver_id = UserSerializer()

    class Meta:
        model = InterestRecords
        fields = '__all__'
