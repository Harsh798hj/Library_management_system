from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (('customer','Customer'), ('librarian','Librarian'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    cover_url = models.URLField(blank=False, null=False)
    total_issued_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(default=timezone.now)

class IssuedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField()
    returned = models.BooleanField(default=False)
    price_at_issue = models.DecimalField(max_digits=8, decimal_places=2)

class SavedForLater(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(default=timezone.now)
