# models.py
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=50)

    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    number_rating= models.IntegerField(default=0)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return self.title


class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    description = models.CharField(max_length=200, null = True)
    created = models.DateTimeField(auto_now_add=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE,related_name="reviews" )
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  str(self.pk)+ " | " + str(self.rating) + " - " +self.watchlist.title + " | " +str(self.review_user)

































# from django.db import models
#
# class StreamPlatform(models.Model):
#     name = models.CharField(max_length=50)
#     about = models.CharField(max_length=150)
#     website = models.URLField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
# class WatchList(models.Model):
#     title = models.CharField(max_length=50)
#     storyline = models.CharField(max_length=200)
#     active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist", default=1)
#
#     def __str__(self): # if we call the string related field it wil return this function
#         return self.title
#



# from django.db import models
#
# class StreamPlatform(models.Model):
#     name = models.CharField(max_length=50)
#     about = models.CharField(max_length=150)
#     website = models.URLField(max_length=50)
#
#     def __str__(self):
#         return self.name
#
# class WatchList(models.Model):
#     title = models.CharField(max_length=50)
#     storyline = models.CharField(max_length=200)
#     active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
#
#     def __str__(self):
#         return self.title  # Error: should return self.title, not self.name






# Create your models here.
# class Movie(models.Model):
#     name = models.CharField(max_length=50)
#     description =models.CharField(max_length=200)
#     active = models.BooleanField(default=True)
#
#     def __str__(self):
#         return self.name