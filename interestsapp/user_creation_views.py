from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages

def user_creation(request):
    return render(request, 'user_register.html', {})

def register_user(request):
    if request.method != 'POST':
        messages.info(request, 'Invalid method')
        return redirect('user_creation')

    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    if password1 != password2:
        messages.info(request, 'Passwords mismatch')
        return redirect('user_creation')

    user = User.objects.filter(username=username)
    if user:
        messages.info(request, 'Username already exists')
        return redirect('user_creation')
    
    try:
        user_obj = User.objects.create_user(username = username,
                                        first_name=username,
                                        password = password1,
                                        is_active=True)
        user_obj.save()
        messages.info(request, 'User created successfully')
        return redirect('')
    except Exception as e:
        messages.info(request, 'Oops something went wrong!', {})
        return redirect('user_creation')