from django import forms
from backend.models import Artist
from backend.models import Album


class SimpleForm(forms.Form):

    value = forms.IntegerField(required=True, label='value', help_text='Enter a value between 1 and 10')

    def save(self):
        return True

    def clean_value(self):
        value = self.cleaned_data['value']
        if value is not None:
            if value < 1 or value > 10:
                raise forms.ValidationError('This value is not accepteble')
        return value


class ArtistCreateForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'description',
            'notes',
        ]


class ArtistUpdateForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = [
            'description',
            'notes',
        ]


class ArtistEditForm(forms.ModelForm):
    """
    To be used for both creation and update
    """

    class Meta:
        model = Artist
        fields = [
            'description',
            'notes',
        ]


class AlbumEditForm(forms.ModelForm):
    """
    To be used for both creation and update
    """

    class Meta:
        model = Album
        fields = [
            'description',
            'artist',
            'year',
        ]
