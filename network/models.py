from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Post(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField( default=0)




    def serialize(self):
        return {
            "username": self.username,
           "text": self.text,

           "likes": self.likes,

           "date": self.date.strftime("%b %d %Y, %I:%M %p"),
        }

class Following(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    subscription= models.ForeignKey(User,on_delete=models.CASCADE, related_name='subs', default='')
    subat=models.IntegerField(null=True, blank=True)
    subto=models.IntegerField(null=True, blank=True)


    def __str__(self):
        return str(self.username)


class Liked(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    liked=models.BooleanField(default=False)
    unliked=models.BooleanField(default=False)

    class Meta:
        unique_together = ('username', 'post', 'liked')
        unique_together = ('username','post', 'unliked')

    def serialize(self):
        return {
            "username": self.username,
            "post": self.post,

            "liked": self.liked,

            "unliked": self.unliked,
        }
#class Verification(models.Model):
    # your fields here
 #   class Meta:
  #      unique_together = [("asset_code", "status)]




