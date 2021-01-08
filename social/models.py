from django.db import models
from django.contrib.auth.models import User

# User profile created at the time of register using signals
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    profile_pic = models.ImageField(
        upload_to='profile_pics/', default="/profile_pics/default.png")

    def __str__(self):
        return str(self.user)

# a single Instasohor post with caption and a image
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='content/', blank=False, null=False)
    liked_users = models.ManyToManyField(User, related_name="liked_users")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.caption)

# user follower, following relationship maintains
class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

# comment
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=450)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

# comment
# like
