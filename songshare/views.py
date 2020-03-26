from django.shortcuts import render

def login_action(request):
    context = {}
    return render(request, 'songshare/login_page.html',context)