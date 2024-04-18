from django import forms
from .models import MedicalInsuranceCost


class InsuranceForm(forms.Form):
    class Meta:
        model = MedicalInsuranceCost
        fields = ['name', 'age', 'sex', 'cost', 'smoker', 'bmi', 'children', 'region']