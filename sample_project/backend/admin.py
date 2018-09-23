from django.contrib import admin
from django.utils import timezone
from .models import Artist
from .models import Album
from .models import Song


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base class for 'shared' model admins;
    manages common metadata
    """
    list_display = ['__str__', ]
    search_fields = ['=id', 'description']
    #readonly_fields = ['id', ]


@admin.register(Artist)
class ArtistAdmin(BaseModelAdmin):
    pass


@admin.register(Album)
class AlbumAdmin(BaseModelAdmin):
    pass


@admin.register(Song)
class SongAdmin(BaseModelAdmin):
    pass
