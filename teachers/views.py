from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from coaching_system_be.auth_utils import get_teacher
from .models import Batch, Teacher
from .serializers import BatchSerializer, TeacherSerializer


class TeacherAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can view teacher data."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TeacherSerializer([teacher], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_current_teacher(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return None, Response({"detail": "Only teachers can access this endpoint."}, status=status.HTTP_403_FORBIDDEN)
        return teacher, None

    def get(self, request, pk):
        teacher, error = self._get_current_teacher(request)
        if error:
            return error
        if teacher.id != pk:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teacher, error = self._get_current_teacher(request)
        if error:
            return error
        if teacher.id != pk:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TeacherSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teacher, error = self._get_current_teacher(request)
        if error:
            return error
        if teacher.id != pk:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        teacher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BatchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can manage batches."}, status=status.HTTP_403_FORBIDDEN)
        queryset = Batch.objects.filter(id=teacher.batch_id).order_by("-created_at")
        serializer = BatchSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        teacher = get_teacher(request.user)
        if not teacher:
            return Response({"detail": "Only teachers can create batches."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BatchSerializer(data=request.data)
        if serializer.is_valid():
            batch = serializer.save()
            teacher.batch = batch
            teacher.save(update_fields=["batch"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BatchDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def _teacher_batch(self, request, pk):
        teacher = get_teacher(request.user)
        if not teacher:
            return None, Response({"detail": "Only teachers can manage batches."}, status=status.HTTP_403_FORBIDDEN)
        batch = get_object_or_404(Batch, pk=pk)
        if teacher.batch_id != batch.id:
            return None, Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return batch, None

    def get(self, request, pk):
        obj, error = self._teacher_batch(request, pk)
        if error:
            return error
        serializer = BatchSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        obj, error = self._teacher_batch(request, pk)
        if error:
            return error
        serializer = BatchSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj, error = self._teacher_batch(request, pk)
        if error:
            return error
        teacher = get_teacher(request.user)
        teacher.batch = None
        teacher.save(update_fields=["batch"])
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
