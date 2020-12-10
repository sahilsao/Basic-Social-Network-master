from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    liked_by = models.ManyToManyField(User, related_name="likes")
    total_likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.content[0:16].strip()}...] by {self.user}"


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.follower} follows {self.following}"

    class Meta:
        unique_together = ['follower', 'following']
