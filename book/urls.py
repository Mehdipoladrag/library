from django.urls import path
from .views import TestView

app_name = 'book'


urlpatterns = [
    path('test/', TestView.as_view()),
]
