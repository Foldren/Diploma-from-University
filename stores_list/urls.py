from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Index),
    re_path(r'^store-', views.ActionRenderSelectStore),
]
