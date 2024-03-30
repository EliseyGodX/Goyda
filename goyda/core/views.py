from django.shortcuts import render

def general(request):
    context = {'test': 123}
    return render(request, 'core/general.html', context)