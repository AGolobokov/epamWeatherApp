from .models import City
from django.forms import ModelForm, TextInput, DateInput


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'start_date', 'end_date']
        widgets = {'name': TextInput(attrs={
            'class': 'form-control',
            'name': 'city',
            'id': 'city',
            'placeholder': 'Input city'
        }), 'start_date': DateInput(attrs={
            'class': 'form-control',
            'name': 'start date',
            'placeholder': 'Example: 2020-08-29'}),
            'end_date': DateInput(attrs={
                'class': 'form-control',
                'name': 'end date',
                'placeholder': 'Example: 2021-08-29'})}
