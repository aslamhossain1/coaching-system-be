from django.urls import path

from .views import FeeAPIView, FeeDetailAPIView

urlpatterns = [
    path("", FeeAPIView.as_view(), name="fee-list-create"),
    path("<int:pk>/", FeeDetailAPIView.as_view(), name="fee-detail"),
]
