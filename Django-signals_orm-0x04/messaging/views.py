from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
@login_required
def delte_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')