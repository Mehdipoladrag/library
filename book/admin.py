from django.contrib import admin
from .models import BookModel, ReviewModel
# Register your models here.


@admin.register(BookModel)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'genre']


@admin.register(ReviewModel)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating']