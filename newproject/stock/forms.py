from django import forms

class StockForm( forms.Form):
    title = forms.CharField( label= "Stock symbol", widget=forms.TextInput(attrs={"autocomplete":"off"}), help_text="Ex：1803.JP")
    day_start = forms.CharField( label = "Start", widget=forms.TextInput(attrs={"autocomplete":"off"}), help_text="Ex：2019-02-01")
    day_end = forms.CharField( label = "End", widget=forms.TextInput(attrs={"autocomplete":"off"}), help_text = "Ex：2020-02-01")