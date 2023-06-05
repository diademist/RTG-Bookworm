
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import BookForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)



class FormBookForm(forms.ModelForm):
    class Meta:
        model= BookForm
        fields= ["bookname", "author", "description", "genre"]