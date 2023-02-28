from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')

class ModelBase(models.Model):
    subject = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.subject

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name

class Course(ModelBase):
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ("subject", 'category')
        # ordering =["-id"]

class Lesson(ModelBase):
    content = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL, related_name="lessons")
    tag = models.ManyToManyField('Tag', null=True, blank=True, related_name='lessons')
    def __str__(self):
        return self.subject

    class Meta:
        unique_together = ("subject", 'course')

class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content = models.TextField()
    lesson = models.ForeignKey(Lesson, related_name='comments', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering =["-id"]

class ActionBase(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        unique_together = ("lesson", "creator")

class Action(ActionBase):
    LIKE, DISLIKE, LOVE = range(3)
    ACTIONS = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
        (LOVE, 'Love')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)

class Rating(ActionBase):
    rate = models.PositiveSmallIntegerField(default=0)
