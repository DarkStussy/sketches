from django import forms

from .models import Service


class OrderForm(forms.Form):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label='Услуга')
    description = forms.CharField(label="Описание заказа", widget=forms.Textarea())
    phone_number = forms.CharField(label="Номер телефона")
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="Изображения")


class AddExampleImageForm(forms.Form):
    image_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                               label="Эскизы")
