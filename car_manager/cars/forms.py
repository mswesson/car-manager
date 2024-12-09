from django import forms

from .models import Car, CarComment


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ["make", "model", "year", "description"]


class CommentCarForm(forms.ModelForm):
    class Meta:
        model = CarComment
        fields = ["content"]
