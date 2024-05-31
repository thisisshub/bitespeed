from . import views
from django.urls import path

urlpatterns = [
    path("identify/", views.IdentifyViewSet.as_view({"post": "create"}), name="identify"),
]