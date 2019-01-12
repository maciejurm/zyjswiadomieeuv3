from django.forms import ModelForm
from bootstrap_datepicker_plus import DateTimePickerInput
from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('author', 'active', 'created_at', 'edited', 'slug')
        widgets = {
            'date_start': DateTimePickerInput(options={"locale": "pl",}),
            'date_end': DateTimePickerInput(options={"locale": "pl",}),
        }