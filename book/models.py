from django.db import models
from accounts.models import CustomUser

# Create your models here.


class BookModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=50)

    class Meta:
        unique_together = ("title", "author", "genre")
        db_table = "books"

    def __str__(self):
        return f"{self.title} by {self.author}"


class ReviewModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name="rating_range",
            ),
            models.UniqueConstraint(
                fields=["book", "user"], name="unique_user_book_review"
            ),
        ]

        db_table = "reviews"

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}"
