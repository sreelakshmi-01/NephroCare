from django import forms
from .models import *

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['title', 'description', 'image']

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question']
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Your message here...',
                                              'style': 'width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 5px; font-size: 14px; height: 100px;'})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['question'].label = False

class DialysisCenterForm(forms.ModelForm):
    class Meta:
        model = DialysisCenter
        fields = ['name', 'full_address', 'district', 'email', 'phone_number']

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['hosp_name', 'city', 'district', 'email', 'phone_no']

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = __all__