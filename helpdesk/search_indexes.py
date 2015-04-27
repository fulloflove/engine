import datetime
from haystack import indexes
from models import Issue


class IssueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    external_id = indexes.CharField(model_attr='external_id')
    subject = indexes.CharField(model_attr='subject')

    def get_model(self):
        return Issue

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(created__lte=datetime.datetime.now())