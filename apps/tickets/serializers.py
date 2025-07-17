from rest_framework.serializers import ModelSerializer, SlugRelatedField


from apps.tickets.models import Attachment, Ticket, User


class AttachmentSerializer(ModelSerializer):
    class Meta:
        model = Attachment
        fields = [
            "id",
            "file",
            "created_at",
            "updated_at",
        ]


class TicketListSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "service",
            "status",
            "priority",
            "updated_at",
        ]


class TicketRetrieveSerializer(ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    issuer = SlugRelatedField(
        many=False,
        slug_field="company__title",
        queryset=User.objects.all(),
    )

    class Meta:
        model = Ticket
        fields = [
            "id",
            "issuer",
            "title",
            "description",
            "service",
            "status",
            "priority",
            "attachments",
            "created_at",
            "updated_at",
        ]
