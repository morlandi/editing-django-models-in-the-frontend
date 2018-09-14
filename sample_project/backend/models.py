import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings


class BaseModel(models.Model):
    """
    Base class for all models; defines common metadata
    """
    class Meta:
        abstract = True

    # Primary key
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
        null=False, blank=False, editable=False)
    description = models.CharField('description', max_length=256, null=False, blank=False)

    def __str__(self):
        text = str(self.id)
        if self.description:
            text = self.description
        return text


class Artist(BaseModel):

    notes = models.TextField(null=False, blank=True)

    class Meta(BaseModel.Meta):
        abstract = False


class Album(BaseModel):

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=False, blank=False)
    year = models.IntegerField(null=True, blank=True)

    class Meta(BaseModel.Meta):
        abstract = False
