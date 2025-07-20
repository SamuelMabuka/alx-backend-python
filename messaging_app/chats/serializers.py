from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework.exceptions import ValidationError  # <- Required

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # <- Required

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    message_body = serializers.CharField()  # <- Required

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]

    def validate_message_body(self, value):
        if not value.strip():
            raise ValidationError("Message body cannot be empty.")  # <- Required
        return value


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]

            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at'
        ]

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
        ]

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages'
        ]
