from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer

from . import serializers


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class Mypage(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.UserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            email = request.data.get("email")
            if email:
                raise ParseError("이메일은 변경할 수 없습니다!")
            user = serializer.save()
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request):
        user = request.user
        if user:
            user.delete()
            return Response("삭제완료!", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_418_IM_A_TEAPOT)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            raise ParseError("비밀번호를 적어주세요!")
        if old_password == new_password:
            raise ParseError("원래와 다른 비밀번호를 적어주세요!")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer