from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coaching_system_be.auth_utils import get_guardian, get_student, get_teacher
from .models import Exam
from .serializers import ExamSerializer


class ExamAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)

        if teacher:
            queryset = Exam.objects.filter(teacher=teacher).order_by("-exam_date")
        elif student:
            queryset = Exam.objects.filter(teacher__batch_id=student.batch_id).order_by("-exam_date")
        elif guardian:
            batch_ids = guardian.students.values_list("batch_id", flat=True)
            queryset = Exam.objects.filter(teacher__batch_id__in=batch_ids).order_by("-exam_date")
        else:
            return Response({"detail": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ExamSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can create exams."}, status=status.HTTP_403_FORBIDDEN)

        payload = request.data.copy()
        payload["teacher"] = teacher.id
        serializer = ExamSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        obj = get_object_or_404(Exam, pk=pk)
        teacher = get_teacher(request.user)
        student = get_student(request.user)
        guardian = get_guardian(request.user)

        allowed = (
            (teacher and obj.teacher_id == teacher.id)
            or (student and obj.teacher and obj.teacher.batch_id == student.batch_id)
            or (guardian and obj.teacher and guardian.students.filter(batch_id=obj.teacher.batch_id).exists())
        )
        if not allowed:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ExamSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can update exams."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Exam, pk=pk)
        if obj.teacher_id != teacher.id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

        payload = request.data.copy()
        payload["teacher"] = teacher.id
        serializer = ExamSerializer(obj, data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can delete exams."}, status=status.HTTP_403_FORBIDDEN)

        obj = get_object_or_404(Exam, pk=pk)
        if obj.teacher_id != teacher.id:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
