from rest_framework import serializers
from rest_framework import serializers
from .models import Ticket, Agent, Department, TicketAnswer, TicketComment


class TicketCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["comment"]


    def create(self, validated_data):
        # 'ticket' and 'answer' are provided via the context
        ticket = self.context.get('ticket')
        # Set ticket directly in validated_data
        validated_data['ticket'] = ticket
        return TicketComment.objects.create(**validated_data)


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["comment", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class TicketAnswerSerializer(serializers.ModelSerializer):
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = TicketAnswer
        fields = ["id", "agent", "comment",
                  "created_at", "updated_at", "comments"]
        read_only_fields = ["created_at", "updated_at",]


class TicketSerializer(serializers.ModelSerializer):
    answers = TicketAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "subject", "comment", "service",
                  "department", "status", "priority", "answers"]
        read_only_fields = ["answers"]
