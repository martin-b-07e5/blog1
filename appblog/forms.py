from django import forms
from .models import Post, Comment

# esto revisar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


# campos que aparecen al agregar un nuevo post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category' ,'title', 'text', 'status')
#        fields = ('title', 'text', 'image')


# campos que aparecen al agregar un nuevo comentario en post existente
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


# by NPA esto revisar
class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario','class': 'form-control', }))
    password = forms.CharField(max_length=50,required=True,widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', 'name': 'password', }))

    class Meta:
        model = User
        fields = ['username', 'contraseña', 'remember_me']
