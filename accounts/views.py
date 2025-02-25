from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        if User.objects.filter(username=data['username']).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(
            username=data['username'],
            password=data['password']
        )
        user.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    # permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract the refresh token from the request body
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            # Blacklist the refresh token
            token.blacklist()
            return Response({"message": "Logout successful"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token or logout failed"}, status=400)
