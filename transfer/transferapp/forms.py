from django import forms
from .models import Transfer, Club
from .models import TransferFormSettings

class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ('class_name', 'seat_number', 'student_name', 'original_club', 'desired_club')
    
    def __init__(self, *args, **kwargs):
        super(TransferForm, self).__init__(*args, **kwargs)
        self.fields['original_club'].queryset = Club.objects.all()
        self.fields['desired_club'].queryset = Club.objects.all()


class TransferFormSettingsForm(forms.ModelForm):
    class Meta:
        model = TransferFormSettings
        fields = ('start_time', 'end_time')