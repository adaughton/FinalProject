from django import forms

from ia_app import models as m


class SIR_Model_Form(forms.Form):
   ## Form fields ##
   S0 = forms.IntegerField(min_value=1, required = True,
      error_messages={'required':'Please enter the initial number susceptible'})
   I0 = forms.IntegerField(min_value=1, required = True,
         error_messages={'required':'Please enter the initial number infected'})
   days_low = forms.IntegerField(min_value = 1,
               widget=forms.Textarea(attrs={'cols':'5', 'rows':'1'}))
   days_high = forms.IntegerField(min_value = 1,
               widget=forms.Textarea(attrs={'cols':'5', 'rows':'1'}))
   r0_low = forms.FloatField(min_value = 0, max_value=20,
               widget=forms.Textarea(attrs={'cols':'5', 'rows':'1'}))
   r0_high = forms.FloatField(min_value = 0, max_value=20,
               widget=forms.Textarea(attrs={'cols':'5', 'rows':'1'}))
   lamb= forms.FloatField(min_value = 0)
   control_start = forms.IntegerField(min_value = 1)
