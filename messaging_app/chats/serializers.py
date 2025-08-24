from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with basic information.
    Used for nested relationships and user listings.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'full_name', 'phone_number', 'role', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        """Return the user's full name."""
        return f"{obj.first_name} {obj.last_name}".strip()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users with password handling.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'password', 'password_confirm'
        ]
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        """Create user with properly hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model with sender information.
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'sender_id', 'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender']
    
    def validate_sender_id(self, value):
        """Validate that sender exists."""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid sender ID.")
        return value


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages with validation.
    """
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']
    
    def validate(self, attrs):
        """Validate that sender is a participant in the conversation."""
        request = self.context.get('request')
        if request and request.user:
            conversation = attrs['conversation']
            if not conversation.participants.filter(id=request.user.id).exists():
                raise serializers.ValidationError(
                    "You are not a participant in this conversation."
                )
        return attrs
    
    def create(self, validated_data):
        """Create message with sender from request user."""
        request = self.context.get('request')
        if request and request.user:
            validated_data['sender'] = request.user
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Basic serializer for Conversation model with participants.
    """
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants', 'participant_ids', 
            'participant_count', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_participant_count(self, obj):
        """Return the number of participants in the conversation."""
        return obj.participants.count()
    
    def validate_participant_ids(self, value):
        """Validate that all participant IDs exist and conversation has at least 2 participants."""
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        
        # Check if all users exist
        existing_users = User.objects.filter(id__in=value)
        if existing_users.count() != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        
        return value
    
    def create(self, validated_data):
        """Create conversation and add participants."""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        
        if participant_ids:
            participants = User.objects.filter(id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation


class ConversationDetailSerializer(ConversationSerializer):
    """
    Detailed serializer for Conversation with nested messages.
    Used for retrieving full conversation details.
    """
    messages = MessageSerializer(many=True, read_only=True)
    latest_message = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = ConversationSerializer.Meta.fields + ['messages', 'latest_message']
    
    def get_latest_message(self, obj):
        """Return the latest message in the conversation."""
        latest = obj.messages.order_by('-sent_at').first()
        if latest:
            return MessageSerializer(latest).data
        return None


class ConversationListSerializer(ConversationSerializer):
    """
    Lightweight serializer for conversation listings.
    Includes only essential information and latest message.
    """
    latest_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta(ConversationSerializer.Meta):
        fields = [
            'conversation_id', 'participants', 'participant_count', 
            'created_at', 'latest_message', 'unread_count'
        ]
    
    def get_latest_message(self, obj):
        """Return the latest message preview."""
        latest = obj.messages.order_by('-sent_at').first()
        if latest:
            return {
                'message_id': latest.message_id,
                'sender_name': latest.sender.get_full_name(),
                'message_body': latest.message_body[:100] + '...' if len(latest.message_body) > 100 else latest.message_body,
                'sent_at': latest.sent_at
            }
        return None
    
    def get_unread_count(self, obj):
        """
        Return unread message count for the requesting user.
        This would require additional model fields to track read status.
        For now, returns 0 as a placeholder.
        """
        # TODO: Implement read status tracking
        return 0


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations with initial message.
    """
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    initial_message = serializers.CharField(
        max_length=1000,
        required=False,
        allow_blank=True
    )
    
    class Meta:
        model = Conversation
        fields = ['participant_ids', 'initial_message']
    
    def validate_participant_ids(self, value):
        """Validate participants and ensure current user is included."""
        request = self.context.get('request')
        if request and request.user:
            # Ensure current user is included in participants
            if request.user.id not in value:
                value.append(request.user.id)
        
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        
        # Check if all users exist
        existing_users = User.objects.filter(id__in=value)
        if existing_users.count() != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        
        return value
    
    def create(self, validated_data):
        """Create conversation with participants and optional initial message."""
        participant_ids = validated_data.pop('participant_ids')
        initial_message = validated_data.pop('initial_message', '')
        
        # Create conversation
        conversation = Conversation.objects.create()
        participants = User.objects.filter(id__in=participant_ids)
        conversation.participants.set(participants)
        
        # Create initial message if provided
        if initial_message and self.context.get('request'):
            Message.objects.create(
                sender=self.context['request'].user,
                conversation=conversation,
                message_body=initial_message
            )
        
        return conversation


# Utility serializers for specific use cases
class ConversationParticipantSerializer(serializers.Serializer):
    """
    Serializer for adding/removing participants from a conversation.
    """
    participant_ids = serializers.ListField(
        child=serializers.UUIDField()
    )
    action = serializers.ChoiceField(choices=['add', 'remove'])
    
    def validate_participant_ids(self, value):
        """Validate that all participant IDs exist."""
        existing_users = User.objects.filter(id__in=value)
        if existing_users.count() != len(value):
            raise serializers.ValidationError("One or more participant IDs are invalid.")
        return value


class MessageBulkSerializer(serializers.Serializer):
    """
    Serializer for bulk operations on messages.
    """
    message_ids = serializers.ListField(
        child=serializers.UUIDField()
    )
    action = serializers.ChoiceField(choices=['delete', 'mark_read'])
    
    def validate_message_ids(self, value):
        """Validate that all message IDs exist and belong to user's conversations."""
        request = self.context.get('request')
        if request and request.user:
            user_conversations = Conversation.objects.filter(participants=request.user)
            valid_messages = Message.objects.filter(
                message_id__in=value,
                conversation__in=user_conversations
            )
            if valid_messages.count() != len(value):
                raise serializers.ValidationError(
                    "One or more message IDs are invalid or not accessible."
                )
        return value