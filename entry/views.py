from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Visitor
from .serializers import VisitorSerializer
import json
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

 
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()

@csrf_exempt
def login_user(request):
     
    if request.method != 'POST':
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    
    user = authenticate(request, username=user_obj.username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    login(request, user)
     
    refresh = RefreshToken.for_user(user)
    access = str(refresh.access_token)

    return JsonResponse({
        "message": f"Login successful! Welcome, {user.get_full_name()}",
        "email": user.email,
        "username": user.username,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser,
        "refresh": str(refresh),
        "access": access
    }, status=200)


 
@csrf_exempt
def logout_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)
    try:
        data = json.loads(request.body.decode('utf-8'))
        refresh_token = data.get("refresh")
    except Exception:
        refresh_token = None
    logout(request)
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()   
        except TokenError:
            return JsonResponse({"error": "Invalid or expired refresh token."}, status=400)
        except Exception:
            return JsonResponse({"error": "Logout failed while blacklisting token."}, status=400)
    return JsonResponse({"message": "Logged out successfully."}, status=200)


 
class EntryView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            visitors = Visitor.objects.all() 
            serializer = VisitorSerializer(visitors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        data = request.data.copy()
        data.pop('entry_time', None)
        serializer = VisitorSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Visitor entry created successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        if request.user.is_authenticated and request.user.is_superuser:
            try:
                visitor = Visitor.objects.get(pk=pk)
                visitor.delete()
                return Response({"message": "Visitor entry deleted successfully."}, status=status.HTTP_200_OK)
            except Visitor.DoesNotExist:
                return Response({"error": "Visitor entry not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
