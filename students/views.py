from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coaching_system_be.auth_utils import can_access_student, get_guardian, get_teacher
from .models import Guardian, Student
from .serializers import GuardianSerializer, StudentSerializer


class StudentAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        teacher = get_teacher(request.user)
        guardian = get_guardian(request.user)
        student = getattr(request.user, "student_profile", None)

        if teacher:
            queryset = Student.objects.filter(batch_id=teacher.batch_id).order_by("-created_at")
        elif student:
            queryset = Student.objects.filter(id=student.id)
        elif guardian:
            queryset = Student.objects.filter(guardian=guardian).order_by("-created_at")
        else:
            return Response({"detail": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)

        serializer = StudentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        teacher = get_teacher(request.user)
        payload = request.data.copy()

        if teacher:
            if not teacher.batch_id:
                return Response({"detail": "Teacher is not assigned to a batch."}, status=status.HTTP_400_BAD_REQUEST)
            payload["batch"] = teacher.batch_id

        serializer = StudentSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(Student, pk=pk)
        if not can_access_student(request.user, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = StudentSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can update student data."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Student, pk=pk)
        if not can_access_student(request.user, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        payload = request.data.copy()
        payload["batch"] = teacher.batch_id
        serializer = StudentSerializer(obj, data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can delete students."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Student, pk=pk)
        if not can_access_student(request.user, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GuardianAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        teacher = get_teacher(request.user)
        guardian = get_guardian(request.user)

        if teacher:
            queryset = Guardian.objects.filter(students__batch_id=teacher.batch_id).distinct().order_by("-created_at")
        elif guardian:
            queryset = Guardian.objects.filter(id=guardian.id)
        else:
            return Response({"detail": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)

        serializer = GuardianSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuardianDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _can_access_guardian(self, request, guardian_obj):
        teacher = get_teacher(request.user)
        guardian = get_guardian(request.user)

        if guardian and guardian.id == guardian_obj.id:
            return True
        if teacher:
            return guardian_obj.students.filter(batch_id=teacher.batch_id).exists()
        return False

    def get(self, request, pk):
        obj = get_object_or_404(Guardian, pk=pk)
        if not self._can_access_guardian(request, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = GuardianSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj = get_object_or_404(Guardian, pk=pk)
        if not self._can_access_guardian(request, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = GuardianSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can delete guardians."}, status=status.HTTP_403_FORBIDDEN)
        obj = get_object_or_404(Guardian, pk=pk)
        if not self._can_access_guardian(request, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
