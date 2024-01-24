from django import forms


from product.config import prohibited_products
from product.models import Product, Version


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('user_own', 'is_published')

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        if cleaned_data.lower() in prohibited_products:
            raise forms.ValidationError('В названии присутствует запрещенное слово')

        return cleaned_data



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_published':
                field.widget.attrs['class'] = 'form-control'


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_relevant':
                field.widget.attrs['class'] = 'form-control'

class ModeratorForm(ProductForm, forms.ModelForm):
    class Meta:
        model = Product
        fields = ('description', 'category', 'is_published')
