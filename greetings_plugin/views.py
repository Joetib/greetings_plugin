from django.shortcuts import render
from .models import Greeting
from .seializers import GreetingSerializer
from django.db.models import QuerySet
# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import HttpRequest
from auth_backends.backends import EdXOAuth2
import requests
import logging
logger = logging.getLogger(__name__)
class GreetingsViewSet(ListCreateAPIView,RetrieveAPIView):
    model = Greeting
    queryset = Greeting.objects.all()
    serializer_class = GreetingSerializer
    permission_classes = [IsAuthenticated]
    authentication_backends  = [
        EdXOAuth2
    ]


    def get_queryset(self) ->  QuerySet[Greeting]:
        queryset: QuerySet[Greeting] = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)
    
    def create(self, request: HttpRequest, *args, **kwargs):
        serializer: GreetingSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        greeting_text = serializer.validated_data["text"]
        logging.info(f"Greeting from {request.user.username}: {greeting_text}")
        self.perform_create(serializer)
        response = {}
        if greeting_text == "hello":
            print(request.build_absolute_uri(request.get_full_path()))
            response = requests.post( request.build_absolute_uri(request.get_full_path()), json={"text": "goodbye"})
            response = {"reply_for_world": response.json()}
        headers = self.get_success_headers(serializer.data)
        return Response({
                **response,
                **serializer.data,
            }, status=status.HTTP_201_CREATED, headers=headers,
        )
    
    def perform_create(self, serializer: GreetingSerializer) -> None:
        return serializer.save(user=self.request.user)

class GreetingsView(GenericAPIView):
    odel = Greeting
    queryset = Greeting.objects.all()
    serializer_class = GreetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self) ->  QuerySet[Greeting]:
        queryset: QuerySet[Greeting] = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

