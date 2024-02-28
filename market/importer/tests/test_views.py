from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from importer.models import ImportLog


class ImporterViewsTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_importer_views(self):
        client = Client()

        # Test ImportPageView
        import_page_url = reverse("importer:import-page")
        import_page_response = client.get(import_page_url)
        self.assertEqual(import_page_response.status_code, 200)

        # Test StartImportView - GET request
        start_import_url = reverse("importer:start-import")
        start_import_response_get = client.get(start_import_url)
        self.assertEqual(start_import_response_get.status_code, 200)

        # Test StartImportView - POST request
        start_import_response_post = self._perform_start_import_request(client, start_import_url)
        self.assertEqual(start_import_response_post.status_code, 200)

        # Test ImportDetailsView
        import_log = ImportLog.objects.create(user=self.user)
        import_details_url = reverse("importer:import-details", kwargs={"import_id": import_log.id})
        import_details_response = client.get(import_details_url)
        self.assertEqual(import_details_response.status_code, 200)

        # Test DownloadCSVTemplateView
        download_csv_url = reverse("importer:download-csv-template")
        download_csv_response = client.get(download_csv_url)
        self.assertEqual(download_csv_response.status_code, 200)

    def _perform_start_import_request(self, client, url):
        client.login(username="testuser", password="testpassword")
        csv_content = (
            "name,main-category,category,description,tag1,price,remains\nProduct1,Category1,Subcategory1,"
            "Description1,Tag1,10,20"
        )
        csv_file = SimpleUploadedFile("test_file.csv", csv_content.encode("utf-8"), content_type="text/csv")
        return client.post(url, {"importFile": csv_file, "subcategoryName": "ValidSubcategory"})
