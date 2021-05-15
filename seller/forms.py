from django import forms
from .models import *

# create a ModelForm
class addProductForm(forms.ModelForm):
    class Meta:
        # Specify the name of Model to use
        model=Product
        fields="__all__"