from django import forms
from .models import TrainingRecord

class RecordForm(forms.ModelForm):
    class Meta:
        model = TrainingRecord
        fields = ['date', 'part', 'name', 'weight', 'reps']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'part': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '例: ベンチプレス'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
        }