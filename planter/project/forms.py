
from django import forms
from .models import WateringLog


class WaterPlantForm(forms.ModelForm):
    class Meta:
        model = WateringLog
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'capture=camera,image/*',
            }),
        }