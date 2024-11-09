# serializers.py
from rest_framework import serializers
from .models import Ticket, Agent, Department, TicketAnswer, TicketComment


class TicketAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketAnswer
        fields = [
            "agent",
            "comment",
            "created_at",
            "updated_at",
        ]


class TicketCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = [
            "comment",
            "created_at",
            "updated_at",
        ]


class TicketSerializer(serializers.ModelSerializer):
    answers = TicketAnswerSerializer(many=True, read_only=True)
    comments = TicketCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "subject",
            "comment",
            "service",
            "department",
            "status",
            "priority",
            "answers",
            "comments",
        ]
