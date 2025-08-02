from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import prefetch

# Create your views here.
@login_required
def delete_user(request):
    if request.method != 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return redirect('profile')

def threaded_messages_view(request):
    # Get all top-level messages (not replies)
    messages = Message.objects.filter(parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    
    return render(request, 'messages/threaded.html', {'messages': messages})