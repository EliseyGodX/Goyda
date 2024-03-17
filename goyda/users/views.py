from django.shortcuts import render

def login(request):
    context = {'title': 'Loging'}
    return render(request, 'users/login.html', context)

def registration(request):
    context = {'title': 'Registration'}
    return render(request, 'users/registration.html', context)