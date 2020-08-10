import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Blogger(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=False
        )
    bio = models.TextField(
        max_length=400,
        help_text='Enter your bio here'
        )

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Returns the url to access a detail record for this blogger."""
        return reverse('blog:blogger-detail', args=[str(self.id)])


class UserText(models.Model):
    """An abstract class describing a text written by a
    registered user with a post date"""
    author = models.ForeignKey(
        Blogger,
        on_delete=models.CASCADE,
        null=False,
        blank=False
        )
    date = models.DateTimeField(default=datetime.datetime.now())
    content = models.TextField()

    class Meta:
        abstract = True


class Post(UserText):
    """A blog post."""
    title = models.CharField(max_length=200)
    content = models.TextField(
        max_length=5000,
        help_text='Enter the post content.'
        )

    def get_absolute_url(self):
        """Returns the url to access a detail record for this post."""
        return reverse('blog:post-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Comment(UserText):
    """A blog comment."""
    content = models.TextField(
        max_length=1000
        )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
        )

    def __str__(self):
        """
        String for representing the Model object.
        """
        len_title = 75
        if len(self.content) > len_title:
            titlestring = self.content[:len_title] + '...'
        else:
            titlestring = self.content
        return titlestring

    class Meta:
        ordering = ['date']
