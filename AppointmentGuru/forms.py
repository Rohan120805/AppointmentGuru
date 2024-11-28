from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.HiddenInput(),
            'comments': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }