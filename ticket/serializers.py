# serializers.py
from rest_framework import serializers
from .models import Ticket, Agent, Department


# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = ['id', 'user', 'department', 'subject', 'description',
#                   'priority', 'status', 'created_at', 'updated_at']
#         read_only_fields = ['user', 'status', 'created_at', 'updated_at']

#     def validate(self, data):
#         if 'priority' in data and data['priority'] == Ticket.PRIORITY_HIGH:
#             data['priority'] = 'high'
#         return data

class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['subject', 'service', 'department', 'status', 'priority']

    def create(self, validated_data):
        # Get the request object to access the current user
        request = self.context['request']
        # Set the user to the currently authenticated user
        validated_data['user'] = request.user
        # Create and return the new Ticket instance
        return super().create(validated_data)
        # Exclude created_at and updated_at fields on creation


class TicketRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'  # Include all fields for retrieval


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'department']
