from django.shortcuts import render

def home(request):
    return render(request, 'lots/lots.html')