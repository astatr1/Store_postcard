from django import forms

POSTCARD_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class BasketAddPostcardForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=POSTCARD_QUANTITY_CHOICES,
                                      coerce=int)
    override = forms.BooleanField(required=False, initial=False,
                                  widget=forms.HiddenInput)
