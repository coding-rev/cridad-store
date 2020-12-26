from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

PAYMENT_CHOICES =(
    ('MOMO','Mobile Money'),
    ('Check','Check Payment')
)
REGION=[
    ('AR','Ashanti'),
    ('GA','Greater Accra'),
    ('WN','Western North'),
    ('B','Bono'),
    ('A','Ahafo'),
    ('O','Oti'),
    ('BE','Bono East'),
    ('NR','North East'),
    ('S','Savannah'),
    ('UE','Upper East'),
    ('C','Central'),
    ('UW','Upper West'),
    ('E','Eastern'),
    ('V','Volta'),
    ('W','Western'),
    ('N','Northern'),
]

COUNTRY = {
    ('Ghana','Ghana')
}

class CheckoutForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRY)
    street_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St',
        'class':'form-control'
    }))
    apartment_address = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Appartment or Suite',
        'class':'form-control'
    }))
    town = forms.CharField(required=True, widget=forms.TextInput (attrs={
        'placeholder':'Town/City',
        'class':'form-control'
    }))
    region = forms.ChoiceField(choices=REGION)

    zip = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder':'Postal Address/Zip',
        'class':'form-control'
    }))
    save_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(required=True,
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name','last_name','email']
        #, 'password1', 'password2'