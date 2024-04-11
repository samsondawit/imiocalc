from django import forms
from .models import Materials, Metalextractiondata


class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = '__all__'  # Use all fields from the model


class MetalForm(forms.ModelForm):
    class Meta:
        model = Metalextractiondata
        fields = '__all__'  # Use all fields from the model