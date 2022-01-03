from django.shortcuts import render, redirect, get_object_or_404
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


@api_view(("GET", "POST"))
@permission_classes((IsAuthenticated,))
def url_list(request):
    if request.method == "GET":
        paginator = PageNumberPagination()
        paginator.page_size = 10
        urls = request.user.urls.all()
        result_page = paginator.paginate_queryset(urls, request)
        serializer = URLSerializer(result_page, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET", "PUT", "DELETE"))
@permission_classes((IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly))
def url_detail(request, pk):
    url = get_object_or_404(URL, pk=pk)
    if request.method == "GET":
        serializer = URLSerializer(url)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = URLSerializer(url, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        url.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("POST",))
def user_create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
