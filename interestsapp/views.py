# Create your views here.
from .models import InterestRecords
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .serializers import InterestRecordsSerializer

def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'user_login.html', {})

def user_login(request):
    context = dict()
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    try:
        user_obj = User.objects.get(username=username)
    except Exception as e:
        messages.info(request, 'User not found')
        return redirect('')
    
    try:
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('')
    except Exception as e:
        messages.error(request, 'An error occurred during authentication')
        return redirect('')
    
@login_required
def dashboard(request):
    users = User.objects.exclude(id=request.user.id)
    received_interests = InterestRecords.objects.filter(receiver_id=request.user)
    sent_interests = InterestRecords.objects.filter(sender_id=request.user)
    
    received_data = InterestRecordsSerializer(received_interests, many=True).data
    sent_data = InterestRecordsSerializer(sent_interests, many=True).data

    context = {
        'user_list': users,
        'received_interests': received_data,
        'sent_interests': sent_data
    }

    return render(request, 'user_dashboard.html', context)

def chat_room(request, sender_id, receiver_id):
    current_user = request.user
    receiver_obj = get_object_or_404(User, id=receiver_id)
    return render(request, 'user_chat.html', {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'current_user': request.user,
        'receiver_username':receiver_obj.username
    })

@login_required
def logout(request):
    auth.logout(request)
    return redirect('')

