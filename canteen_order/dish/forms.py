from django import forms

class DishForm(forms.Form):
    dish_name = forms.CharField(max_length=16, label='菜品名', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    dish_intro = forms.CharField(max_length=128, label='食材', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    dish_price = forms.IntegerField(label='价格')
    dish_store = forms.IntegerField(label='库存')
