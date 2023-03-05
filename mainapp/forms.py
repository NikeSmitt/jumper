from django import forms

from mainapp.models.product import Product


class ProductSearchForm(forms.ModelForm):
    """Форма для поиска товаров в header"""
    name = forms.CharField(
        max_length=200,
        min_length=1,
        widget=forms.TextInput(attrs={'placeholder': 'Найди свои любимые вещи'})
    )
    
    class Meta:
        model = Product
        fields = ['name',]
        