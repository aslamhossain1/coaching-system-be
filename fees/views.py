from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coaching_system_be.auth_utils import get_guardian, get_student, get_teacher
from .models import Fee
from .serializers import FeeSerializer


class FeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)

        if teacher:
            queryset = Fee.objects.filter(student__batch_id=teacher.batch_id).order_by("-created_at")
        elif student:
            queryset = Fee.objects.filter(student=student).order_by("-created_at")
        elif guardian:
            queryset = Fee.objects.filter(student__guardian=guardian).order_by("-created_at")
        else:
            return Response({"detail": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FeeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can create fees."}, status=status.HTTP_403_FORBIDDEN)

        serializer = FeeSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["student"].batch_id != teacher.batch_id:
                return Response({"detail": "Student is not in your batch."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeeDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_object(self, pk):
        return get_object_or_404(Fee, pk=pk)

    def _can_read(self, request, obj):
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)
        return (
            (teacher and obj.student.batch_id == teacher.batch_id)
            or (student and obj.student_id == student.id)
            or (guardian and obj.student.guardian_id == guardian.id)
        )

    def get(self, request, pk):
        obj = self._get_object(pk)
        if not self._can_read(request, obj):
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = FeeSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can update fees."}, status=status.HTTP_403_FORBIDDEN)

        obj = self._get_object(pk)
        if obj.student.batch_id != teacher.batch_id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = FeeSerializer(obj, data=request.data)
        if serializer.is_valid():
            if serializer.validated_data["student"].batch_id != teacher.batch_id:
                return Response({"detail": "Student is not in your batch."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can delete fees."}, status=status.HTTP_403_FORBIDDEN)

        obj = self._get_object(pk)
        if obj.student.batch_id != teacher.batch_id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
