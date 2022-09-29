from django.forms import ModelForm

from chatapp.models import LandingChat


class LandingChatForm(ModelForm):
    class Meta:
        model = LandingChat
        fields = ['writer', 'date', 'chat']
        error_messages = {
            'chat': {
                'required': '메세지를 입력해주세요!'
            },
        }
