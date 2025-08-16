from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from django.db.models import Count

User = get_user_model() # Get the currently active user model


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name',
            'username', 'bio', 'is_online', 'last_login']
        read_only_fields = ['user_id', 'is_online', 'last_login', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)


    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender',
                  'message_body', 'sent_at', 'is_read']
        read_only_fields = ['message_id', 'sender', 'sent_at', 'is_read']


class ConversationSerializer(serializers.ModelSerializer):
    target_user_id = serializers.UUIDField(write_only=True, required=True)
    display_participants = UserSerializer(source='participants', many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'name', 'messages', 'created_at', 'target_user_id',
                  'display_participants']
        read_only_fields = ['url', 'conversation_id', 'target_user_id', 'created_at']

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True, context=self.context).data

    def create(self, validated_data):
        target_user_uuid = validated_data.pop('target_user_id')
        request_user = self.context['request'].user

        # Fetch the target User instance
        try:
            other_participant_user = User.objects.get(user_id=target_user_uuid)
        except User.DoesNotExist:
            raise serializers.ValidationError({"target_user_id": "User with this ID does not exist."})

        # Prevent creating a conversation with self
        if request_user == other_participant_user:
            raise serializers.ValidationError({"target_user_id": "Cannot start a conversation with yourself."})

        # Define the two participants for the conversation
        all_participants_for_conversation = [request_user, other_participant_user]

        # Check for existing conversation between these two specific users
        existing_conversation = Conversation.objects.filter(
            participants__in=all_participants_for_conversation
        ).annotate(
            num_distinct_participants=Count('participants', distinct=True)
        ).filter(
            num_distinct_participants=2
        ).first()

        if existing_conversation:
            return existing_conversation
        else:
            conversation_name = validated_data.get('name')
            conversation = Conversation.objects.create(name=conversation_name)
            conversation.participants.set(all_participants_for_conversation)

            return conversation
