# wardrobe/forms.py

from django import forms
from .models import WardrobeItem
# wardrobe/forms.py

from django import forms

class OutfitSuggestionForm(forms.Form):
    occasion_choices = [
        ('Casual', 'Casual'),
        ('formal', 'Formal'),
        ('party', 'Party'),
        # Add more choices as needed
    ]

    occasion = forms.ChoiceField(choices=occasion_choices, label='Occasion')
    location = forms.CharField(max_length=100, label='Location')

class WardrobeItemForm(forms.ModelForm):
    class Meta:
        model = WardrobeItem
        fields = []
