from django.urls import path, include
from .views import TestView

app_name = 'book'


urlpatterns = [
    path('test/', TestView.as_view()),
    path('api/', include('book.api.urls')),
]
