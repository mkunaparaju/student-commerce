from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Book, Tag, Reservation
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('name', 'avail_start', 'avail_end')
        widgets = {
            'avail_start': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3),
            'avail_end': DateTimeWidget(attrs={'id':"datetimeid"}, usel10n = True, bootstrap_version=3)
       }

class EditBookForm(forms.ModelForm):
	
	# def __init__(self, *args, **kwargs):
	# 	self.user = user

 #        super(EditBookForm, self).__init__(*args, **kwargs)
 #        self.fields['name'].initial = book.name
 #        self.fields['avail_start'].initial = book.avail_start
 #        self.fields['avail_end'].initial = book.avail_end

    
	class Meta:
		model = Book
		fields = ('name', 'avail_start', 'avail_end')
		widgets = {
            'avail_start': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3),
            'avail_end': DateTimeWidget(attrs={'id':"datetimeid"}, usel10n = True, bootstrap_version=3)
       }

class ReserveForm(forms.ModelForm):
	#reserved_start = forms.DateTimeField(widget=AdminDateWidget())
	# reserved_start = forms.DateTimeFeild(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
	class Meta:
		model = Reservation
		fields = ('reserved_start', 'duration')
		widgets = {
            'reserved_start': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
       }

	
		 		
	

class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data