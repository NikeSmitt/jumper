from django import forms

from orderapp.models import Order


class LogoutCreateOrderForm(forms.ModelForm):
    
    placeholders = {
        'phone': 'Телефон',
        'email': 'Email',
        'first_name': 'Имя',
        'last_name': 'Фамилия',
        'address': 'Адрес',
        'city': 'Город'
    }

    class Meta:
        model = Order
        exclude = ('created_at', 'order_number')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            
            field.field.widget.attrs['placeholder'] = self.placeholders.get(field.name)
            field.field.widget.attrs['class'] = 'form-control'
    