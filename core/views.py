from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import URL
from .permissions import IsOwnerOrReadOnly
from .serializers import URLSerializer, UserSerializer


def url(request, code):
    u = get_object_or_404(URL, code=code)
    u.click()
    return redirect(u.url)


class URLList(generics.ListCreateAPIView):
    serializer_class = URLSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.urls.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class URLDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = URL.objects.all()
    serializer_class = URLSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
