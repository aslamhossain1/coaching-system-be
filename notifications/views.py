from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coaching_system_be.auth_utils import get_guardian, get_student, get_teacher
from .models import Notification
from .serializers import NotificationSerializer


class NotificationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)

        if teacher:
            queryset = Notification.objects.filter(student__batch_id=teacher.batch_id).order_by("-created_at")
        elif student:
            queryset = Notification.objects.filter(student=student).order_by("-created_at")
        elif guardian:
            queryset = Notification.objects.filter(student__guardian=guardian).order_by("-created_at")
        else:
            return Response({"detail": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can create notifications."}, status=status.HTTP_403_FORBIDDEN)

        payload = request.data.copy()
        payload["teacher"] = teacher.id
        serializer = NotificationSerializer(data=payload)
        if serializer.is_valid():
            student = serializer.validated_data.get("student")
            if student and student.batch_id != teacher.batch_id:
                return Response({"detail": "Student is not in your batch."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(Notification, pk=pk)
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)

        allowed = (
            (teacher and obj.student and obj.student.batch_id == teacher.batch_id)
            or (student and obj.student_id == student.id)
            or (guardian and obj.student and obj.student.guardian_id == guardian.id)
        )
        if not allowed:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        serializer = NotificationSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can update notifications."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Notification, pk=pk)
        if not obj.student or obj.student.batch_id != teacher.batch_id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        payload = request.data.copy()
        payload["teacher"] = teacher.id
        serializer = NotificationSerializer(obj, data=payload)
        if serializer.is_valid():
            student_obj = serializer.validated_data.get("student")
            if student_obj and student_obj.batch_id != teacher.batch_id:
                return Response({"detail": "Student is not in your batch."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can delete notifications."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Notification, pk=pk)
        if not obj.student or obj.student.batch_id != teacher.batch_id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
