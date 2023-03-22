from django. forms import ModelForm
from django import forms
from datetime import datetime
from .models import Registration, User
from django.contrib.auth.forms import UserCreationForm
from .models import Event


class RegistrationForm(ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'email']


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',  'first_name', 'last_name', 'password1', 'password2')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'category', 'location', 'price', 'date_time', 'featured_image')
        widgets = {
            'location': forms.TextInput(attrs={'id': 'location-input', 'placeholder': 'Enter location'}),
        }

    date_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %I:%M %p'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )


    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        try:
            # Convert datetime object to string
            date_time_str = date_time.strftime('%Y-%m-%d %I:%M %p')
            # Convert to datetime object
            dt_obj = datetime.strptime(date_time_str, '%Y-%m-%d %I:%M %p')
            # Convert to ISO format string
            iso_format = dt_obj.isoformat()
            return iso_format
        except ValueError:
            raise forms.ValidationError('Invalid date and time format')
        
    
    def save(self, commit=True, user=None):
        event = super().save(commit=False)
        event.creator = user
        if commit:
            event.save()
        return event
