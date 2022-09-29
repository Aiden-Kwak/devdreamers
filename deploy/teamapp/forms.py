from datetime import datetime, timezone

from django import forms
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget

from teamapp.models import Team


class TeamCreationForm(ModelForm):
    content = forms.CharField(widget=SummernoteWidget(), initial='<p>(작성 예시 - 참고용)</p>'
                                                                 '<ol>'
                                                                 '<li>팀 소개 (팀의 목적 및 방향성에 대해 설명합니다!)</li>'
                                                                 '<li>기술 스택 (Vue.js, Django, Pytorch와 같이 어떤 기술스택을 사용할 예정인가요?)</li>'
                                                                 '<li>이런 분들을 원합니다! (어떤 인재가 이 팀에 필요한가요?)</li>'
                                                                 '<li>진행현황 (현재까지의 진행현황을 지원자들이 알 수 있겠죠?)</li>'
                                                                 '<li>모집 인원 (어떤 분야에서 몇 명을 뽑을 계획이신가요?)</li>'
                                                                 '<li>지원 방법 및 절차 (지원자가 어떻게 지원할 수 있나요?)</li>'
                                                                 '<li>기타사항</li>'
                                                                 '</ol>')
    class Meta:
        model = Team
        # fields = ['title', 'description', 'image', 'type', 'content', 'category', 'contact', 'team_color', 'deadline']
        fields = ['title', 'description', 'image', 'type', 'content', 'category', 'contact', 'team_color', 'deadline', 'to_open']

        error_messages = {
            'title': {
                'required': '팀이름은 필수입력사항입니다!'
            },
            'description': {
                'required': '한줄소개는 필수입력사항입니다!'
            },
            'image': {
                'required': '사진을 등록해주세요!'
            },
            'type': {
                'required': '팀 유형을 선택해주세요!'
            },
            'content': {
                'required': '팀 설명은 필수입력사항입니다!'
            },
            'contact': {
                'required': '연락처는 필수입력사항입니다!'
            },
            'deadline': {
                'required': '모집 마감일을 선택해주세요!'
            },
            'category': {
                'required': '모집 분야를 선택해주세요!'
            },

        }


class SearchForm(forms.Form):
    word = forms.CharField(label='')



