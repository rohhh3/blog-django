from typing import Any
from django import forms
from .models import Post, Category, CustomUser, Comment
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions

form_control_widget = forms.TextInput(attrs={'class': 'form-control'})

class UpdateUserForm(UserChangeForm):
    username = forms.CharField(widget=form_control_widget, required=False)
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control"}), required=False)
    first_name = forms.CharField(widget=form_control_widget, max_length=128, required=False)
    last_name = forms.CharField(widget=form_control_widget, max_length=128, required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}), max_length=512, required=False)
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control-file"}))
    password = None

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'description', 'avatar']

    def __init__(self, *args: Any, **kwargs: Any):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
    
class UpdateUserPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=form_control_widget)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")
        if confirm_password and password and confirm_password != password:
            raise ValidationError("Passwords do not match.")
        return confirm_password
    
class LoginForm(forms.Form):
    username = forms.CharField(widget=form_control_widget)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise ValidationError("Invalid username or password")
        return cleaned_data

    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"})
        }

class PostForm(forms.ModelForm):
    MAX_IMAGE_SIZE = 8 * 1024 * 1024 
    MAX_IMAGE_DIMENSION = 2048 

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple, 
        required=True  
    )
    def clean_thumbnail(self):
        thumbnail = self.cleaned_data.get('thumbnail')
        
        if thumbnail:
            if thumbnail.size > self.MAX_IMAGE_SIZE:
                raise ValidationError(_('The image size should be less than 8MB.'))
            
            width, height = get_image_dimensions(thumbnail)
            if width > self.MAX_IMAGE_DIMENSION or height > self.MAX_IMAGE_DIMENSION:
                raise ValidationError(_('The image dimensions should be less than 2048x2048px.'))

            return thumbnail
        else:
            return thumbnail
        
    class Meta:
        model = Post
        fields = ('isPublic', 'password', 'title', 'content', 'categories', 'thumbnail')

        widgets = {
            'isPublic': forms.CheckboxInput(attrs={'id': 'isPublicCheckbox'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'passwordInput'}),
            'title': form_control_widget,
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }