from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'answer', 'image_width']

        labels = {
            'question': '',
            'answer':'',
            #'image':'',
            'image_width':'',
        }

        widgets = {
            'question': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Fråga'}),
            'answer': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'Svar'}),
            #'image': forms.FileInput(attrs={'class':'form-control', 'placeholder': 'Bild'}),
            'image_width': forms.NumberInput(attrs={'class':'form-control', 'placeholder': 'Bildbredd i %'}),
        }