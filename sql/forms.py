from .models import InstanceUser
from django.forms import ModelForm


class InstanceUserFrom(ModelForm):

    class Meta:
        model = InstanceUser
        fields = [
            'instance', 'user', 'user_host', 'password', 'schema', 'tables', 'status'
        ]
        help_texts = {
            'instance': '* required',
            'user': '* required',
            'user_host': '* required',
            'password': '* required',
            'schema': '* required',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super('InstanceUserFrom',self).__init__(*args, **kwargs)