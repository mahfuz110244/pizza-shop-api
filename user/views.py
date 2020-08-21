from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Customer
from .serializers import CustomerSerializer, CustomerLoginSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginAPIView(APIView):
    """
    User Login in Pizza App. Existing User can login with his Phone number and Password.
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        response = {}
        try:
            username = request.data.get('phone', "")
            request.data['username'] = username
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                # Get all the necessary data as response
                user = Customer.objects.get(username=username)
                refresh = TokenObtainPairSerializer.get_token(user)
                serializer_user = CustomerLoginSerializer(user)
                response = serializer_user.data
                response['jwt_token'] = str(refresh.access_token)
                return Response(response, status=status.HTTP_200_OK)
            else:
                # response['message'] = str(serializer.errors)
                response['msg'] = "Unauthorized"
                return Response(response, status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            response['msg'] = str(e)
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    """
    Retrieve, update a Customer instance.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        user_details = {
            "name": user.name,
            "phone": user.username,
            "address": user.address,
            "current_location": {
                "lat": user.latitude,
                "lng": user.longitude
            }
        }
        response = user_details
        return Response(response, status=status.HTTP_200_OK)

    def patch(self, request):
        response = {}
        user = request.user
        username = request.data.get('phone', "")
        current_location = request.data.get('current_location', "")
        if username:
            request.data['username'] = username
        if current_location:
            request.data['latitude'] = current_location['lat']
            request.data['longitude'] = current_location['lng']

        serializer = CustomerSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response['msg'] = "OK"
            return Response(response, status=status.HTTP_200_OK)
        response['err'] = str(serializer.errors)
        return Response(response, status.HTTP_400_BAD_REQUEST)
