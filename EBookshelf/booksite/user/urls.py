#User/urls.py
from django.urls import include, re_path, path
from user.views import *

urlpatterns = [
    re_path(r"^accounts/", include("django.contrib.auth.urls")),
    re_path(r"^dashboard/", dashboard, name="dashboard"),
    re_path(r"^register/", register, name="register"),
    re_path(r"^bookform/", bookaddform, name="bookform"),
    path('delete_book/<id>', delete_book, name='delete_book'),
]
