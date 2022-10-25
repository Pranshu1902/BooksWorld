from email.policy import default
from django.db import models
from django.contrib.auth.models import User
#import uuid

# Create your models here.

STATUS_CHOICES = (
    ("Reading", "Reading"),
    ("Completed", "Completed"),
    ("Abandoned", "Abandoned"),
)

class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    imageLink = models.CharField(max_length=3500, default="http://books-world-pranshu1902.herokuapp.com/static/default.png", null=True, blank=True)
    user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE, null=True, blank=True)
    totalPages = models.IntegerField(default=0)
    pagesRead = models.IntegerField(default=0)
    timeTaken = models.IntegerField(default=0)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    
    # image = models.ImageField(default="default.png", upload_to="book_images")
    # id = models.UUIDField(primary_key=True, unique=True)#, default=uuid.uuid4, editable=False)
    # reading = models.BooleanField(default=False)
    # date_started = models.DateField(auto_now_add=True, null=True, blank=True)
    # date_finished = models.DateField(null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
