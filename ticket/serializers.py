from rest_framework import serializers
from rest_framework import serializers

from core.models import Service
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


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name']  # Or any other relevant fields


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class TicketDetailSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    department = DepartmentSerializer()
    answers = TicketAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = ["id", "subject", "comment", "service",
                  "department", "status", "priority", "answers", "updated_at", "attached_file"]
        read_only_fields = ["answers"]


class TicketListSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Ticket
        fields = ["id", "subject", "service",
                  "department", "status", "priority", "updated_at"]


class TicketCreateSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    department = DepartmentSerializer()

    class Meta:
        model = Ticket
        fields = ["subject", "comment", "service",
                  "department", "status", "priority", "attached_file"]

    def create(self, validated_data):
        service_data = validated_data.pop('service')
        department_data = validated_data.pop('department')

        # Get or create the related service and department
        service = Service.objects.get_or_create(name=service_data["name"])[0]
        department = Department.objects.get_or_create(
            name=department_data["name"])[0]

        # Create the ticket with related fields
        ticket = Ticket.objects.create(
            service=service, department=department, **validated_data)
        return ticket
