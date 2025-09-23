from django.db import models
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage


# Create your models here.

class Country(models.Model):
    country_name = models.CharField(max_length=50, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    class Meta:
        db_table = 'countries'
    
    def __str__(self):
        return self.country_name
    

class City(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    city_name = models.CharField(max_length=40)
    
    class Meta:
        db_table = 'city'
    
    def __str__(self):
        return self.city_name

    
class Visit(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(storage=MediaCloudinaryStorage())
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='visits', null=True) 
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)   
    
    class Meta:
        db_table = 'visits'
    
    def __str__(self):
        return self.content
    
    

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    visit = models.ForeignKey(Visit, on_delete= models.CASCADE, related_name='comments')
    
    class Meta:
        db_table = 'comments'
    
    def __str__(self):
        return self.content
    
    
    
class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(Comment, on_delete= models.CASCADE, related_name='likes')
    
    class Meta:
        db_table = 'comment_likes'
    
    def __str__(self):
        return f'{self.user.username} liked {self.comment}'
    

class VisitLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_likes')
    visit = models.ForeignKey(Visit, on_delete= models.CASCADE, related_name='likes')
    
    class Meta:
        db_table = 'visit_likes'
    
    def __str__(self):
        return f'{self.user.username} liked {self.visit}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(storage=MediaCloudinaryStorage(),blank=True, null=True)
    bio = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'profile'
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete= models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete= models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'follow'
        unique_together = ('follower', 'following') 
    
    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'
    