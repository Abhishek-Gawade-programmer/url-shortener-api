from django.urls import path
from .views import *

app_name = "core"

urlpatterns = [
    path("urls/", url_list, name="url_list"),
    path("urls/<int:pk>/", url_detail, name="url_detail"),
    path("<code>/", url, name="url"),
]
