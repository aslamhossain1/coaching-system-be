from django.urls import path

from .views import HomeworkAPIView, HomeworkDetailAPIView

urlpatterns = [
    path("", HomeworkAPIView.as_view(), name="homework-list-create"),
    path("<int:pk>/", HomeworkDetailAPIView.as_view(), name="homework-detail"),
]
