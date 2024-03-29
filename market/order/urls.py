from django.urls import path
from .views import (
    FirstOrderView,
    SecondOrderView,
    ThirdOrderView,
    FourStepView,
    OrderListView,
    OrderDetailView,
)

app_name = "order"

urlpatterns = [
    path("step/", FirstOrderView.as_view(), name="step1"),
    path("step1/", SecondOrderView.as_view(), name="step2"),
    path("step2/", ThirdOrderView.as_view(), name="step3"),
    path("step3/", FourStepView.as_view(), name="step4"),
    path("history/", OrderListView.as_view(), name="history_order"),
    path("history/<int:pk>/", OrderDetailView.as_view(), name="detail_order"),
]
