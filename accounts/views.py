from rest_framework import generics, permissions, status
from accounts.serializers import RegisterSerializer, CookieTokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated


ACCESS_TOKEN_LIFETIME_SECONDS = 5 * 60
REFRESH_TOKEN_LIFETIME_SECONDS = 7 * 24 * 60 * 60

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        res = Response({'detail': 'User registered and logged in.'}, status=status.HTTP_201_CREATED)

        res.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=ACCESS_TOKEN_LIFETIME_SECONDS
        )

        res.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=REFRESH_TOKEN_LIFETIME_SECONDS
        )

        return res


class CustomTokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"refresh": ["Refresh token not found in cookies."]}, status=400)

        serializer = CookieTokenRefreshSerializer(data={'refresh': refresh_token}, context={'request': request})

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get("access")
        refresh_token = serializer.validated_data.get("refresh")

        response = Response({"detail": "Tokens refreshed and stored in cookies."})

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=ACCESS_TOKEN_LIFETIME_SECONDS
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=REFRESH_TOKEN_LIFETIME_SECONDS
        )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access_token = serializer.validated_data.get('access')
        refresh_token = serializer.validated_data.get('refresh')

        response = Response({"detail": "Login successful. Tokens stored in cookies."}, status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=ACCESS_TOKEN_LIFETIME_SECONDS
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=REFRESH_TOKEN_LIFETIME_SECONDS
        )

        return response


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return Response({"detail": "No refresh token found"}, status=status.HTTP_400_BAD_REQUEST)

            token = OutstandingToken.objects.get(token=refresh_token)
            BlacklistedToken.objects.create(token=token)

            response = Response({"detail": "Logged out successfully"}, status=status.HTTP_200_OK)
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except OutstandingToken.DoesNotExist:
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)