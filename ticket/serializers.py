from rest_framework import serializers

from ticket.models import Ticket, Department, TicketAnswer, TicketComment

from core.models import Service



class TicketCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketComment
        fields = ["comment"]

    def create(self, validated_data):

        ticket = self.context.get('ticket')

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
        fields = ['name']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']



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
                  "department", "status", "priority"]
        
    def create(self, validated_data):
        service_data = validated_data.pop('service')
        department_data = validated_data.pop('department')

        
        service = Service.objects.get_or_create(name=service_data["name"])[0]
        department = Department.objects.get_or_create(
            name=department_data["name"])[0]

        
        ticket = Ticket.objects.create(
            service=service, department=department, **validated_data)
        return ticket



class TicketChatSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    agent = serializers.IntegerField(required=False) 
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
    

    class Meta:
        model = Ticket
        fields = [
            "id", "subject", "comment", "service", "department", "status",
            "priority", "updated_at", "created_at"]