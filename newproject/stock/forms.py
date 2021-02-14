from django import forms

class StockForm( forms.Form):
    title = forms.CharField( label= "銘柄", widget=forms.TextInput(attrs={"autocomplete":"off"}))
    day_start = forms.CharField( label = "開始日時", widget=forms.TextInput(attrs={"autocomplete":"off"}))
    day_end = forms.CharField( label = "終了日時", widget=forms.TextInput(attrs={"autocomplete":"off"}))