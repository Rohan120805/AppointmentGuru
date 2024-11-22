from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comments']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(6)]),
            'comments': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }