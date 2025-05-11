import os

from django.http import FileResponse, Http404
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def serve_file(request, file_path):
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    if not os.path.exists(full_file_path):
        raise Http404("File not found")

    return FileResponse(open(full_file_path, "rb"))
