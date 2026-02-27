from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .auth_utils import get_guardian, get_student, get_teacher


User = get_user_model()

# Make sure these functions return the related profile object or None
def get_teacher(user):
    return getattr(user, "teacher_profile", None)

def get_student(user):
    return getattr(user, "student_profile", None)

def get_guardian(user):
    return getattr(user, "guardian_profile", None)

class RoleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get("role")
        email = request.data.get("email")
        password = request.data.get("password")

        # Basic validation
        if role not in {"teacher", "student", "guardian"}:
            return Response({"detail": "role must be teacher, student, or guardian."}, status=status.HTTP_400_BAD_REQUEST)
        if not email or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate using email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Check role
        role_obj = None
        if role == "teacher":
            role_obj = get_teacher(user)
        elif role == "student":
            role_obj = get_student(user)
        elif role == "guardian":
            role_obj = get_guardian(user)

        if role_obj is None:
            return Response({"detail": f"User is not registered as {role}."}, status=status.HTTP_403_FORBIDDEN)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
            "profile_id": role_obj.id,
        }, status=status.HTTP_200_OK)
