# serializers.py
from rest_framework import serializers
from .models import Ticket, Agent, Department


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            # "issuer",
            "subject",
            "comment",
            "service",
            "department",
            "status",
            "priority",
        ]
