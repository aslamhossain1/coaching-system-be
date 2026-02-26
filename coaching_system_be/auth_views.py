from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .auth_utils import get_guardian, get_student, get_teacher


class RoleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get("role")
        email = request.data.get("email")
        password = request.data.get("password")

        if role not in {"teacher", "student", "guardian"}:
            return Response({"detail": "role must be teacher, student, or guardian."}, status=status.HTTP_400_BAD_REQUEST)
        if not email or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request=request, username=email, password=password)
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        role_obj = None
        if role == "teacher":
            role_obj = get_teacher(user)
        elif role == "student":
            role_obj = get_student(user)
        elif role == "guardian":
            role_obj = get_guardian(user)

        if role_obj is None:
            return Response({"detail": f"User is not registered as {role}."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": role,
                "profile_id": role_obj.id,
            },
            status=status.HTTP_200_OK,
        )

