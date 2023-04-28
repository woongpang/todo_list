from django.utils import timezone
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from .models import TodoList
from .serializers import TodoSerializer, TodoDetailSerializer, TodoDetailListSerializer


class TodoLists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = settings.PAGE_SIZE
        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size
        all_todolists = TodoList.objects.filter(user=request.user)
        serializer = TodoSerializer(
            all_todolists[start:end],
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = TodoDetailSerializer(data=request.data)
        if serializer.is_valid():
            todolist = serializer.save(
                user=request.user,
            )
            serializer = TodoDetailSerializer(todolist)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class TodoListDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return TodoList.objects.get(pk=pk, user=user)
        except TodoList.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        todolist = self.get_object(pk, request.user)
        serializer = TodoDetailListSerializer(todolist)
        return Response(serializer.data)

    def delete(self, request, pk):
        todolist = self.get_object(pk, request.user)
        todolist.delete()
        return Response("삭제 완료!", status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        todolist = self.get_object(pk, request.user)
        serializer = TodoDetailListSerializer(
            todolist,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            updated_at = request.data.get("updated_at")
            completion_at = request.data.get("completion_at")
            is_complete = request.data.get("is_complete")
            if updated_at or completion_at:
                raise ParseError("업데이트 시간과 완료 시간은 설정이 불가합니다.")
            if is_complete == False or is_complete == None:
                completion_at = None
            else:
                completion_at = str(timezone.localtime(timezone.now()).date())
            updated_at = str(timezone.localtime(timezone.now()).date())
            todolist = serializer.save(
                updated_at=updated_at, completion_at=completion_at
            )
            serializer = TodoDetailListSerializer(todolist)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )