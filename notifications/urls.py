from django.urls import path

from .views import NotificationAPIView, NotificationDetailAPIView

urlpatterns = [
    path("", NotificationAPIView.as_view(), name="notification-list-create"),
    path("<int:pk>/", NotificationDetailAPIView.as_view(), name="notification-detail"),
]
