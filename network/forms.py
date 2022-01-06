from django import forms
from django.forms import ModelForm, Textarea

from .models import Post

class PostForm(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = Post
        fields = ['text']
        labels = {
            'text': (''),
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'new_post', 'placeholder': 'What"s happening?'}),
        }


class EditPost(forms.ModelForm):
    class Meta:
        model=Post
        fields =['text']