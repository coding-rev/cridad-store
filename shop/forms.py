from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


REGION=[
    ('Ashanti','Ashanti'),
    ('Greater Accra','Greater Accra'),
    ('Western North','Western North'),
    ('Bono','Bono'),
    ('Ahafo','Ahafo'),
    ('Oti','Oti'),
    ('Bono East','Bono East'),
    ('North East','North East'),
    ('Savannah','Savannah'),
    ('Upper East','Upper East'),
    ('Central','Central'),
    ('Upper West','Upper West'),
    ('Eastern','Eastern'),
    ('Volta','Volta'),
    ('Western','Western'),
    ('Northern','Northern'),
]

COUNTRY = {
    ('Ghana','Ghana')
}

class CheckoutForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRY)
    phone = forms.IntegerField(required=True)
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'',
        'class':'form-control'
    }))
    apartment_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'',
        'class':'form-control'
    }))
    town = forms.CharField(required=True, widget=forms.TextInput (attrs={
        'placeholder':'',
        'class':'form-control'
    }))
    region = forms.ChoiceField(choices=REGION)

    postal = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'',
        'class':'form-control'
    }))
    

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']
        #, 'password1', 'password2'