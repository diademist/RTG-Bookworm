from django.forms import ModelForm
from manager.models import Person


class RegisterForm(ModelForm):
username = forms.CharField(max_length=100)
password = forms.CharField(widget=PasswordInput)
email = forms.CharField(widget=EmailInput)
birthdate = forms.DateField()



    class Meta:
        model = Person
        fields = ["username", "password", "birthdate", "email"]