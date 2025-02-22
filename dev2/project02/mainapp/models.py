from django.db import models
from django.contrib.auth.models import User
import os

class Thought(models.Model):
    title = models.CharField(max_length=150)
    content = models.CharField(max_length=400)
    date_posted = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE)

class Profile(models.Model):
    profile_pic = models.ImageField(null=True, blank=True, default='default.png')
    user = models.ForeignKey(User, max_length=10, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Kiểm tra nếu có ảnh cũ và ảnh mới khác ảnh mặc định
        if self.pk:
            old_profile = Profile.objects.get(pk=self.pk)
            if old_profile.profile_pic != self.profile_pic and old_profile.profile_pic.name != 'default.png':
                if os.path.isfile(old_profile.profile_pic.path):
                    os.remove(old_profile.profile_pic.path)

        super().save(*args, **kwargs)
    