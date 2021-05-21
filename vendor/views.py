#API VIews
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import CustomUser, Vendor
from .permissions import IsVendor
from .serializers import UserSerializer, VendorSerializer, ConfirmAccountSerializer, UserLoginSerializer



# List and Create vendors
class VendorList(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# Get details of a vendor
class VendorDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

# Confirm user account
class ConfirmAccount(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmAccountSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

    # Handle cases where confirmation code is not attached to an account
        
        try:
            user = CustomUser.objects.get(
                confirmation_code=serializer.data["confirmation_code"]
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User account does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        # handle cases where account is already confirmed
        user = CustomUser.objects.get(
                confirmation_code=serializer.data["confirmation_code"]
            )

        if user.is_confirmed:
            return Response(
                {"detail": "User account already confirmed!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        

        # confirm account
        user.is_confirmed = True
        user.active = True
        user.save()

        # open shop
        if user.user_type == 'VENDOR':
            vendor = get_object_or_404(Vendor, user=user)
            vendor.closed = False
            vendor.save()

        


        return Response(
            {"detail": "Account confirmed successfully!"}, status=status.HTTP_200_OK
        )

#Login User
class VendorLogin(CreateAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            'success' : 'True',
            'status code' : status.HTTP_200_OK,
            'message': 'User logged in  successfully',
            'token' : serializer.data['token'],
            }
        status_code = status.HTTP_200_OK

        return Response(response, status=status_code)

  
class VendorProfile(RetrieveAPIView):
    permission_classes = (IsVendor,)
    authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        vendor = get_object_or_404(Vendor, user=request.user)
        data = VendorSerializer(vendor).data
        return Response(data, status=status.HTTP_200_OK)

