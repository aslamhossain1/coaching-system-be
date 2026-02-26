from django.urls import path

from .views import ExamAPIView, ExamDetailAPIView

urlpatterns = [
    path("", ExamAPIView.as_view(), name="exam-list-create"),
    path("<int:pk>/", ExamDetailAPIView.as_view(), name="exam-detail"),
]
