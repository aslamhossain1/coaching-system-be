from django.urls import path

from .views import AttendanceAPIView, AttendanceDetailAPIView

urlpatterns = [
    path("", AttendanceAPIView.as_view(), name="attendance-list-create"),
    path("<int:pk>/", AttendanceDetailAPIView.as_view(), name="attendance-detail"),
]
