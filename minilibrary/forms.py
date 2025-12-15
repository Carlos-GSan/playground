## archivo para crear mis propios formularios
from django import forms
from .models import Review

class ReviewSimpleForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, max_value=5,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Califica del 1 al 5',
            'class':'form-control'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder':'Escribe tu reseña aquí...',
            'class': 'form-control',
            'rows':4
        })
    )
    
## ModelForm -> Se crea un formulario automáticamente del modelo review,

class ReviewForm(forms.ModelForm):
    # modelo con el que se basa
    class Meta:
        model = Review
        fields = ['rating', 'text']
        
        def clean_rating(self):
            rating = self.cleaned_data['rating']
            if rating < 1 or rating > 5:
                raise forms.ValidationError(
                    "La calificación debe estar entre 1 y 5."
                )
            return rating
        def clean(self):
            cleaned_data = super().clean()
            rating = cleaned_data.get('rating')
            text = cleaned_data.get('text')
            
            if rating == 1 and len(text) < 20:
                raise forms.ValidationError("Si la calificación es de 1 de estrella, por favor explica mejor tu reseña")
            