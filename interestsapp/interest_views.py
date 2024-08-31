# views.py

from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import InterestRecords
from .serializers import InterestRecordsSerializer
from django.contrib.auth.models import User, auth

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendInterest(request):
    user_id = request.POST.get('user_id', '')
    receiver = get_object_or_404(User, id=user_id)
    
    # Check if an interest has already been sent
    if InterestRecords.objects.filter(sender_id__in=[request.user, receiver], receiver_id__in=[request.user, receiver]).exists():
        return JsonResponse({'detail': 'Interest request already exists.'}, status=400)
    
    # Create a new interest request
    interest_request = InterestRecords.objects.create(sender_id=request.user, receiver_id=receiver, status='Pending')
    serializer = InterestRecordsSerializer(interest_request)
    
    return JsonResponse({'msg': 'Interest sent!'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def sendResponse(request):
    interest_id = request.POST.get('interest_id', '')
    interest_status = request.POST.get('interest_status', '')
    interest = get_object_or_404(InterestRecords, interest_id=interest_id, receiver_id=request.user)
    interest.status = interest_status
    interest.save()
    serializer = InterestRecordsSerializer(interest)
    
    return JsonResponse({'msg': 'Interest ' + interest_status + '!'}, status=201)