from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, UserDetailSerializer


class UserAPIView(APIView):
    # 회원가입
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "회원가입이 완료되었습니다.",
                    "code": status.HTTP_201_CREATED,
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    # 회원정보 조회
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    # 회원정보 수정
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserDetailSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "회원정보가 수정되었습니다.",
                    "code": status.HTTP_200_OK,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원정보 삭제
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(
            {"message": "회원정보가 삭제되었습니다.", "code": status.HTTP_204_NO_CONTENT},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserFollowAPIView(APIView):
    # 팔로우
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def post(self, request, pk):
        user = self.get_object(pk)
        user.following.add(request.user)
        return Response(
            {"message": "팔로우가 완료되었습니다.", "code": status.HTTP_200_OK},
            status=status.HTTP_200_OK,
        )

    # 언팔로우
    def delete(self, request, pk):
        user = self.get_object(pk)
        user.following.remove(request.user)
        return Response(
            {"message": "언팔로우가 완료되었습니다.", "code": status.HTTP_204_NO_CONTENT},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserFollowListAPIView(APIView):
    # 팔로잉 리스트
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user.following, many=True)
        return Response(serializer.data)
