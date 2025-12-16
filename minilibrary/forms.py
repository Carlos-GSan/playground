from django import forms
from .models import Review
import re

BAD_WORDS = ["mugroso", "tonto", "wey", "todo wey", "malo"]

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder':'Califica del 1 al 5',
            'class': 'form-control'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder':'Escribe tu reseña aquí...',
            'class': 'form-control',
            'rows': 4
        })
    )
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating','text']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'placeholder': 'Calificación del 1 al 5',
                'class': 'form-control'
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Escribe tu reseña',
                'class': 'form-control',
                'rows':4
            })
        }
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError("El rating debe estar entre 1 y 5")
        return rating
    
    def clean_text(self):
        text = self.cleaned_data['text']
        words = re.findall(r'\b\w+\b', text.lower()) 
        
        for bad_word in BAD_WORDS:
            if bad_word.lower() in words:
                raise forms.ValidationError(f"La reseña contienen una palabra prohibida: {bad_word}")
        return text
    
    def clean(self):
        cleaned_data = super().clean()
        rating = cleaned_data.get("rating")
        text = cleaned_data.get("text") or ''
        
        if rating == 1 and len(text) < 10:
            raise forms.ValidationError("Si la calificación es de una estrella, por favor explica mejor tu reseña")