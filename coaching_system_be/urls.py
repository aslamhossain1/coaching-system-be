from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .auth_views import RoleLoginAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", RoleLoginAPIView.as_view(), name="role_login"),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/students/", include("students.urls")),
    path("api/teachers/", include("teachers.urls")),
    path("api/attendance/", include("attendance.urls")),
    path("api/fees/", include("fees.urls")),
    path("api/exams/", include("exams.urls")),
    path("api/homework/", include("homework.urls")),
    path("api/notifications/", include("notifications.urls")),
]
