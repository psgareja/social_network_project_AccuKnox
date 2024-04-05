
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignupSerializer, UserLoginSerializer, FriendRequestSerializer, UserSerializer
from .models import User, FriendRequest, Friendship
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate user
            user = authenticate(request, username=email, password=password)

            if user:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
            else:
                # Invalid credentials
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def search_users(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        users = User.objects.filter(email__icontains=keyword)[:10]
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    if request.method == 'POST':
        to_user_id = request.data.get('to_user_id')
        try:
            to_user = User.objects.get(id=to_user_id)
            if to_user != request.user:
                friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
                serializer = FriendRequestSerializer(friend_request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "You cannot send a friend request to yourself"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid user ID"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request):
    if request.method == 'POST':
        friend_request_id = request.data.get('friend_request_id')
        if not friend_request_id:
            return Response({"error": "Friend request ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
            friend_request.accepted = True
            friend_request.save()
            return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request):
    if request.method == 'POST':
        friend_request_id = request.data.get('friend_request_id')
        if not friend_request_id:
            return Response({"error": "Friend request ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
            friend_request.delete()
            return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    if request.method == 'GET':
        user = request.user
        friendships1 = Friendship.objects.filter(user1=user)
        friendships2 = Friendship.objects.filter(user2=user)
        friends = list(friendships1.values_list('user2', flat=True)) + list(friendships2.values_list('user1', flat=True))
        friends = User.objects.filter(id__in=friends)
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_friend_requests(request):
    if request.method == 'GET':
        pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
        serializer = FriendRequestSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
