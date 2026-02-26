from django.urls import path

from .views import BatchAPIView, BatchDetailAPIView, TeacherAPIView, TeacherDetailAPIView

urlpatterns = [
    path("", TeacherAPIView.as_view(), name="teacher-list-create"),
    path("<int:pk>/", TeacherDetailAPIView.as_view(), name="teacher-detail"),
    path("batches/", BatchAPIView.as_view(), name="batch-list-create"),
    path("batches/<int:pk>/", BatchDetailAPIView.as_view(), name="batch-detail"),
]
