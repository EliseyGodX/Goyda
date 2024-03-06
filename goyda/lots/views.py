from django.shortcuts import render

def general(request):
    return render(request, 'lots/lots.html')

def lots(request):
    return '1'