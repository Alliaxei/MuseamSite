from django import forms
from .models import Exhibit, User, Hall


class ExhibitForm(forms.ModelForm):
    class Meta:
        model = Exhibit
        fields =['name', 'author', 'origin', 'quantity', 'category', 'history', 'condition', 'hall']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['name', 'login', 'email', 'password']

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = '__all__'