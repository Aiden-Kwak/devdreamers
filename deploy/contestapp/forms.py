from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from contestapp.models import Contest


class ContestCreationForm(ModelForm):
    content = forms.CharField(widget=SummernoteWidget(), initial='<p>(작성 예시 - 참고용)</p>'
                                                                 '<ol>'
                                                                 '<li>접수기간</li>'
                                                                 '<li>지원내용</li>'
                                                                 '<li>공모분야</li>'
                                                                 '<li>공모자격</li>'
                                                                 '<li>작품규격</li>'
                                                                 '<li>제출서류</li>'
                                                                 '<li>제출방법</li>'
                                                                 '</ol>')
    class Meta:
        model = Contest
        fields = ['title', 'host', 'participant', 'homepage', 'category', 'start_date', 'finish_date', 'image']

        error_messages = {
            'title': {
                'required': '공모전명은 필수입력사항입니다!'
            },
            'host': {
                'required': '주최/주관은 필수입력사항입니다!'
            },
            'participant': {
                'required': '공모대상은 필수입력사항입니다!'
            },
            'homepage': {
                'required': '홈페이지 주소를 입력해주세요!'
            },
            'category': {
                'required': '공모전 분야를 선택해주세요!'
            },
            'start_date': {
                'required': '모집 시작일을 선택해주세요!'
            },
            'finish_date': {
                'required': '모집 마감일을 선택해주세요!'
            },
            'image': {
                'required': '공모전 포스터를 등록해주세요!'
            },

        }