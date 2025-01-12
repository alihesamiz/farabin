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


class TicketCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment  
        fields = ["comment", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

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


# class TicketDetailSerializer(serializers.ModelSerializer):
#     service = ServiceSerializer()
#     department = DepartmentSerializer()
#     answers = TicketAnswerSerializer(many=True, read_only=True)
#     comments = TicketCommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Ticket
#         fields = ["id", "subject", "comment", "service",
#                   "department", "status", "priority", "answers", "comments", "updated_at"]#, "attached_file"]
#         read_only_fields = ["answers", "comments"]


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
                  "department", "status", "priority"]#, "attached_file"]

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






class TicketChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    agent = serializers.IntegerField(required=False)  # Only for answers
    comment = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def to_representation(self, instance):
        if isinstance(instance, TicketAnswer):
            return {
                "id": instance.id,
                "type": "answer",
                "agent": instance.agent.id,
                "comment": instance.comment,
                "created_at": instance.created_at,
                "updated_at": instance.updated_at,
            }
        elif isinstance(instance, TicketComment):
            return {
                "id": instance.id,
                "type": "comment",
                "comment": instance.comment,
                "created_at": instance.created_at,
                "updated_at": instance.updated_at,
            }
        return super().to_representation(instance)


class TicketDetailSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    department = DepartmentSerializer()
    chats = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id", "subject", "comment", "service", "department", "status",
            "priority", "chats", "updated_at"
        ]

    def get_chats(self, obj):
        # Combine answers and comments
        answers = obj.answers.all()
        comments = obj.comments.all()
        combined = sorted(
            list(answers) + list(comments), key=lambda x: x.created_at, reverse=False
        )
        serializer = TicketChatSerializer(combined, many=True)
        return serializer.data