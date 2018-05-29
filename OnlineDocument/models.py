from django.db import models
from django.contrib.auth.models import User
from util.storage import DocumentStorage

# Create your models here.
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('文档名称', default='新文档', max_length=50)
    original_file = models.FileField('原始文件地址', upload_to='static/document/original/%Y/%M', storage=DocumentStorage())
    pdf_file = models.FileField('PDF', upload_to='static/document/pdf/%Y/%M', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.IntegerField('浏览量', default=0)
    created_time = models.DateTimeField(default=timezone.now)
    like = models.IntegerField('赞', default=0)
    dislike = models.IntegerField('踩', default=0)

    def __str__(self):
        return self.title


class RateDetail(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_rated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.document.title

    class Meta:
        ordering=['-date']


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ManyToManyField(Document)

    def __str__(self):
        return self.user.profile.nickname


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ManyToManyField(Document)

    def __str__(self):
        return self.user.profile.nickname
