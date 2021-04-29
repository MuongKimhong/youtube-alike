import uuid

from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.text import slugify
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=200)


class UserVideoViewTags(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)


class Video(models.Model):
    uploader    = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.TextField()
    description = models.TextField(blank=True)
    slug        = models.SlugField()
    complex_id  = models.CharField(max_length=150)
    video       = models.FileField(upload_to="user_videos/")
    views       = models.IntegerField(default=0)
    tags        = models.ManyToManyField(Tag, blank=True)
    thumbnail   = models.ImageField(upload_to="user_videos/thumbnails/")
    date        = models.DateTimeField(auto_now_add=True)
    likes       = models.ManyToManyField(User, related_name="like", blank=True)
    dislikes    = models.ManyToManyField(User, related_name="dislike", blank=True)

    def generate_complex_id(self):
        complex_id = uuid.uuid4()

        if Video.objects.filter(complex_id=complex_id).exists():
            self.generate_complex_id()

        return complex_id

    def __str__(self):
        return self.title

    def views_increment(self):
        self.views = self.views + 1
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.complex_id = self.generate_complex_id() 
        super(Video, self).save(*args, **kwargs)


class UserViewedVideo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    videos = models.ManyToManyField(Video, blank=True)


class Comment(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    video    = models.ForeignKey(Video, on_delete=models.CASCADE)
    content  = models.TextField()
    likes    = models.ManyToManyField(User, related_name="commnet_like", blank=True)
    dislikes = models.ManyToManyField(User, related_name="comment_dislike", blank=True)
    date     = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    url     = models.URLField()
