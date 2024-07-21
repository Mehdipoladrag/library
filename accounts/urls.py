from django.urls import path, include
from .views import TestView

app_name = 'accounts'


urlpatterns = [
    path('test/', TestView.as_view()),
    path('api/', include('accounts.api.urls')),
]
