from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile






class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['name', 'email', 'content']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model=User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):


    class Meta:
        model = Profile
        fields = ['image']


class AddPost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['photo', 'title', 'slug', 'author', 'content']

