from django import forms

from .models import Book, Tag

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('name', 'avail_start', 'avail_end')

#class TagForm