import uuid
from django.core.exceptions import PermissionDenied
from django.db import models
from django.utils import timezone
from django.conf import settings
from .utils import increment_revision


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


class Song(BaseModel):

    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=False, blank=False)
    position = models.IntegerField(default=0, null=False, blank=False)

    class Meta(BaseModel.Meta):
        abstract = False
        ordering = ['position', ]

    def clone(self, request=None):

        if request and not request.user.has_perm('backend.add_song'):
            raise PermissionDenied

        obj = Song.objects.get(id=self.id)
        obj.pk = uuid.uuid4()
        obj.description = increment_revision(self.description)
        obj.save()
        return obj
