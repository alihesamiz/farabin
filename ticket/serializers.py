# serializers.py
from rest_framework import serializers
from .models import Ticket, Agent, Department


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'user', 'department', 'subject', 'description',
                  'priority', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def validate(self, data):
        if 'priority' in data and data['priority'] == Ticket.PRIORITY_HIGH:
            data['priority'] = 'high'
        return data


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'department']
