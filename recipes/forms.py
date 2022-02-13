from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'tags', 'favorites', 'cooked', 'ingredients', 'content', 'main_photo', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'favorites': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cooked': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'main_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


