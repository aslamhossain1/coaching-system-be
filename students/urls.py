from django.urls import path

from .views import GuardianAPIView, GuardianDetailAPIView, StudentAPIView, StudentDetailAPIView

urlpatterns = [
    path("", StudentAPIView.as_view(), name="student-list-create"),
    path("<int:pk>/", StudentDetailAPIView.as_view(), name="student-detail"),
    path("guardians/", GuardianAPIView.as_view(), name="guardian-list-create"),
    path("guardians/<int:pk>/", GuardianDetailAPIView.as_view(), name="guardian-detail"),
]
