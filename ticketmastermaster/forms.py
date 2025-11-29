from django import forms
from .models import Event, Post

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'