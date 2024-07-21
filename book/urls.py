from django.urls import path, include

app_name = 'book'


urlpatterns = [
    path('api/', include('book.api.urls')),
]
