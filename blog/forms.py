from django import forms

from .models import Post

class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Leave a comment!"}
        )
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('isPublic', 'title', 'content', 'categories', 'thumbnail')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
        }