from django import forms
from .models import Room, Reservation


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            'name',
            'capacity',
            'is_projector_available',
        )


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = (
            'date',
            # 'room',
            'comment',
        )
        widgets = {
            'date': forms.DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date'}),
        }
