from django.urls import path

from .views import ImportPageView, StartImportView, ImportDetailsView, DownloadCSVTemplateView

app_name = "imports"

urlpatterns = [
    path("import/", ImportPageView.as_view(), name="import-page"),
    path("start-import/", StartImportView.as_view(), name="start-import"),
    path("import-details/<int:pk>/", ImportDetailsView.as_view(), name="import-details"),
    path("download-csv-template/", DownloadCSVTemplateView.as_view(), name="download-csv-template"),
]
