from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.http import require_http_methods
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import os

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def serve_file(request, file_path):
    # Construct the full file path
    full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)

    # Check if the file exists
    if not os.path.exists(full_file_path):
        raise Http404("File not found")

    # Serve the file
    return FileResponse(open(full_file_path, 'rb'))
