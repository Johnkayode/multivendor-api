from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from vendor.models import CustomUser

from .models import Administrator
from .permissions import IsSuperuser
from .serializers import AdminSerializer


class ListandCreateAdmin(generics.ListCreateAPIView):
    permission_classes = (IsSuperuser,)
    queryset = Administrator.objects.all()
    serializer_class = AdminSerializer