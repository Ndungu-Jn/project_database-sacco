from django import forms

from sacco.models import Customer

GENDER_CHOICES =(
    ('Male', 'Male'),
    ('Female','Female'),
)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'dob', 'weight', 'gender']
        widgets = {
            'dob': forms.DateInput(attrs={'type':'date', 'min': '1980-01-01', 'max':'2005-12-31'}),
            'weight':forms.NumberInput(attrs={'type':'number', 'min':'35', 'max':'100'}),
            'gender':forms.Select(choices=GENDER_CHOICES)
           
        }


        
