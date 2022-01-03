from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("api-auth/registration/", UserCreate.as_view(), name="user_create"),
    path("urls/", URLList.as_view(), name="url_list"),
    path("urls/<int:pk>/", URLDetail.as_view(), name="url_detail"),
    path("<code>/", url, name="url"),
]
