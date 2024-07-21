from django.urls import path
from .views import CustomTokenLoginApiView


urlpatterns = [
    path("token/", CustomTokenLoginApiView.as_view()),
]
