from django.contrib import admin
from .models import BookModel, ReviewModel
# Register your models here.

admin.site.register(BookModel)
admin.site.register(ReviewModel)