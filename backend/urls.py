from . import views
from django.urls import path

urlpatterns = [
    path("", views.IdentifyViewSet.as_view({"post": "create"}), name="identify"),
]
