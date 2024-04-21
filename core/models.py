from django.db import models
from accounts.models import  User
# Create your models here.

def get_media_file(instance, filename):
    """
    The function `get_media_file` returns the file path for a media file based on the instance ID and
    filename provided.
    
    :param instance: Instance refers to an instance of a model or class in object-oriented programming.
    In this context, it likely represents an instance of a media file object or entity that is being
    processed or handled within the code snippet provided
    :param filename: The `filename` parameter is a string that represents the name of the file being
    processed or accessed. It could be the name of an image file, video file, audio file, or any other
    type of media file
    :return: The function `get_media_file` is returning a string that represents the file path for a
    media file. The file path is constructed by joining the elements 'images', the ID of the instance,
    and the filename using the '/' separator.
    """
    return '/'.join(['images', str(instance.id),filename])


class Messages(models.Model):
    sender = models.ForeignKey(User, related_name=("sender"), on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name=("receiver"), on_delete=models.CASCADE)
    content = models.TextField()
    media_url = models.ImageField(max_length=255, upload_to=get_media_file, null=True, blank=True, default=None)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        db_table = "Messages"

    def __str__(self):
        return f"Message {self.id} - {self.content[:20]}"