from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=225)
    slug = models.CharField(
        max_length=225,
        unique=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    status = models.IntegerField(
        choices=((0, "Draft"), (1, "Publish"), (2, "Delete")),
        default=0,
    )
    tag = models.ManyToManyField(Tag)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.SET_NULL,
        null=True,
        related_name='post_comment',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='replies'
    )

    def __str__(self):
        return str(self.author) + 'comment' + str(self.content)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
