
from django import forms

from pipes_types.models import PipeType


class UpdateColorSelectForm(forms.Form):

    type_id = forms.IntegerField(required=False)

    def clean_type_id(self):
        type_id = self.cleaned_data.get('type_id')

        try:
            PipeType.objects.get(id=type_id)
        except PipeType.DoesNotExist:
            raise forms.ValidationError("No PipeType with given id")
        return type_id