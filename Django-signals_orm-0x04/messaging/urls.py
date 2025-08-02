from django.urls import path
from .views import delete_user

urlpatterns = [
    path('delete-account/', delete_user, name='delete_user'),
    path('unread/', views.unread_messages_view, name='unread_messages'),
]