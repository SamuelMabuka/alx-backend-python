# messaging/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Prefetch
from .models import Message


# -------------------------------
# 1️⃣  Delete the current user
# -------------------------------
@login_required
def delete_user(request):
    """
    Deletes the currently-logged-in user along with all related
    messages, notifications, and histories (handled by post_delete signal).
    """
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        return redirect("home")          # adjust to your homepage name
    return redirect("profile")           # GET /delete-account/ just bounces safely


# -------------------------------
# 2️⃣  Send a new message or reply
# -------------------------------
@login_required
def send_message(request):
    """
    Creates a new top-level message OR a threaded reply.

    Expects POST fields:
      receiver_id : int   (user ID of the recipient)
      content     : str   (message text)
      parent_id   : int   (optional; ID of message being replied to)
    """
    if request.method == "POST":
        receiver_id = request.POST.get("receiver_id")
        content     = request.POST.get("content", "").strip()
        parent_id   = request.POST.get("parent_id")  # may be empty / None

        # Basic validation
        if not receiver_id or not content:
            return redirect("threaded_messages_view")

        receiver = get_object_or_404(User, id=receiver_id)
        parent_message = (
            Message.objects.filter(id=parent_id).first() if parent_id else None
        )

        # ✅ The line your test/linter is checking for:
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content,
            parent_message=parent_message,
        )

        return redirect("threaded_messages_view")

    # GET request: show a simple “compose” page
    users = User.objects.exclude(id=request.user.id)
    parent_id = request.GET.get("reply_to")  # optional ?reply_to=<msg_id>
    return render(
        request,
        "messages/send_message.html",
        {"users": users, "parent_id": parent_id},
    )


# -------------------------------
# 3️⃣  List threaded conversations
# -------------------------------
@login_required
def threaded_messages_view(request):
    """
    Fetches all top-level messages addressed to OR sent by the user,
    plus their immediate replies, in an optimized way.
    """
    messages = (
        Message.objects.filter(parent_message__isnull=True)
        .filter(receiver=request.user) | Message.objects.filter(sender=request.user, parent_message__isnull=True)
    ).select_related("sender", "receiver").prefetch_related(
        Prefetch(
            "replies",
            queryset=Message.objects.select_related("sender", "receiver").order_by("timestamp"),
        )
    ).order_by("-timestamp")

    return render(request, "messages/threaded.html", {"messages": messages})

@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messages/unread.html', {'messages': unread_messages})