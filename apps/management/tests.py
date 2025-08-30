import io
import tempfile
from openpyxl import Workbook
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.management.models import HumanResource
from apps.company.models import CompanyProfile as Company
from apps.core.models import User




def make_test_excel_file():
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    # Header rows (skipped in parser)
    ws.append(["Header1", "Header2", "Header3", "Header4", "Header5"])
    ws.append(["---", "---", "---", "---", "---"])
    ws.append(["---", "---", "---", "---", "---"])

    # Actual test row (row 4)
    ws.append([
        "Ali",                  # name
        "DEVELOPER",            # position (uppercase expected by parser)
        "MANAGER, TEAM LEAD",   # reports_to_position (comma-separated)
        "DESIGNER, TESTER",     # cooperates_with_position (comma-separated)
        "Obligation1"           # obligations
    ])

    # Optional: add more test rows
    ws.append([
        "Sara",
        "DESIGNER",
        "TEAM LEAD",
        "DEVELOPER",
        "Obligation2"
    ])

    tmp = tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False)
    wb.save(tmp.name)
    tmp.seek(0)
    return tmp




class HumanResourceViewSetTests(APITestCase):
    def setUp(self):
        self.company = Company.objects.get(national_code = '12700000000') 
        self.user = User.objects.get(id = 1)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("human-resources")  # adjust if your router name differs

    @patch("apps.management.serializers.process_personnel_excel")
    def test_create_human_resource_with_excel(self, mock_process_excel):
        excel_file = make_test_excel_file()

        response = self.client.post(
            self.url,
            {"excel_file": excel_file},
            format="multipart",
        )

        # Check response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HumanResource.objects.count(), 1)

        hr = HumanResource.objects.first()
        self.assertEqual(hr.company, self.company)

        # Check that processing function was called
        mock_process_excel.assert_called_once_with(hr.id)


