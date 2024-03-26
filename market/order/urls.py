from django.urls import path
from .views import FirstOrderView, SecondOrderView, ThirdOrderView, FourStepView

app_name = 'urls'

urlpatterns = [
    path("step/", FirstOrderView.as_view(), name="step1"),
    path("step1/", SecondOrderView.as_view(), name="step2"),
    path("step2/", ThirdOrderView.as_view(), name='step3'),
    path("step3/", FourStepView.as_view(), name='step4'),

]
