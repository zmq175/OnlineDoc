import datetime

from haystack import indexes
from .models import Document,Tag
from users.models import Profile


class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.NgramField(use_template=True)
    created_time = indexes.DateTimeField(model_attr='created_time')

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        return Document.objects.filter(created_time__lte=datetime.datetime.now())
