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
        fields = ['hospital', 'name', 'specialization', 'qualification', 'experience', 'phone_no', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['title', 'short_description', 'detailed_description', 'image']

class DietPlanForm(forms.ModelForm):
    class Meta:
        model = DietPlan
        fields = ['stage', 'title', 'short_description', 'detailed_instructions', 'image', 'video_url']

class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['stage', 'title', 'category', 'duration', 'image', 'video_url']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = '__all__'
        widgets = {
            'used_for': forms.Textarea(attrs={'rows': 3}),
            'prescription_required': forms.CheckboxInput(),
        }
