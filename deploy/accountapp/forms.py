from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.contrib.auth import get_user_model, password_validation

from accountapp.models import User, Profile, Activity, Award, Intern, Language, Certificate, AdvertiseMail

date_format = '%Y-%m-%d'

UserModel = get_user_model()


class AccountCreateForm(UserCreationForm):

    error_messages = {'password_mismatch':'비밀번호가 일치하지 않습니다.'}

    class Meta:
        model = User
        fields = ("username", "school", "email", "department", "school_status")
        error_messages = {
            'username': {
                'required': '아이디를 적어주세요!',
                'unique': '아이디가 이미 존재합니다!'
            },
            'school': {
                'required': '학교를 선택해주세요!',
                'invalid_choice': '학교이름은 옵션 중에서 선택해주세요!'
            },
            'email': {
                'required': '이메일을 적어주세요!',
                'invalid': '이메일 형식에 맞게 작성해주세요!',
                'unique': '이메일이 이미 존재합니다!'
            },
            'department': {
                'required': '학과를 적어주세요!'
            },
            'school_status': {
                'required': '재학상태를 선택해주세요!',
                # 'invalid_choice': '재학상태는 옵션 중에서 선택해주세요!'
            }
        }
    # 학교 인증 이메일 확인
    def clean_email(self):
        domain = self.cleaned_data['email'].split('@')[1]
        school = self.cleaned_data['school']
        validation = {'0': ['skku.edu', 'g.skku.edu'],
                      '1': ['gist.ac.kr','gm.gist.ac.kr'],
                      '2': ['sogang.ac.kr'],
                      '3': ['unist.ac.kr'],
                      '4': ['cau.ac.kr'],
                      '5': ['kaist.ac.kr'],
                      '6': ['hanyang.ac.kr'],
                      '7': ['snu.ac.kr'],
                      '8': ['yonsei.ac.kr'],
                      '9': ['korea.ac.kr'],
                      '10': ['khu.ac.kr'],
                      '11': ['hufs.ac.kr'],
                      '12': ['uos.ac.kr'],
                      '13': ['catholic.ac.kr'],
                      '14': ['konkuk.ac.kr'],
                      '15': ['kw.ac.kr'],
                      '16': ['kookmin.ac.kr'],
                      '17': ['dgu.ac.kr', 'dongguk.edu'],
                      '18': ['seoultech.ac.kr'],
                      '19': ['sju.ac.kr', 'sejong.ac.kr'],
                      '20': ['soongsil.ac.kr'],
                      '21': ['hongik.ac.kr'],
                      '22': ['gachon.ac.kr'],
                      '23': ['inha.edu', 'inha.ac.kr'],
                      '24': ['ajou.ac.kr'],
                      '25': ['kau.ac.kr', ' kau.kr'],
                      '26': ['ewhain.net', 'ewha.ac.kr'],
                      '27': ['sungshin.ac.kr'],
                      '28': ['swu.ac.kr', 'swuo365.onmicrosoft.com'],
                      '29': ['sookmyung.ac.kr', 'sm.ac.kr'],
                      '30': ['dongduk.ac.kr'],
                      '31': ['duksung.ac.kr'],
                      '32': ['knua.ac.kr', 'karts.ac.kr'],
                      '33': ['dgist.ac.kr'],
                      '34': ['postech.ac.kr'],
                      '35': ['jnu.ac.kr'],
                      '36': ['handong.edu'],
                      '37': ['cnu.kr', 'cnu.ac.kr'],
                      '38': ['pusan.ac.kr'],
                      }

        valid_email = validation[school]
        if domain not in valid_email:
            raise ValidationError("자신의 학교 계정 이메일을 입력해주세요!")
        return self.cleaned_data['email']

class ChangePasswordForm(UserCreationForm):

    error_messages = {'password_mismatch':'비밀번호가 일치하지 않습니다.'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].disabled = True


class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        label=("이메일"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    id = forms.CharField(label="아이디")


class SetPasswordForm(forms.Form):

    error_messages = {'password_mismatch':'비밀번호가 일치하지 않습니다.'}
    
    new_password1 = forms.CharField(
        label=("새로운 비밀번호"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=("새로운 비밀번호 확인"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        # fields = ['image', 'nickname', 'github', 'email']
        fields = ['image', 'nickname', 'github', 'email', 'to_open']
        error_messages = {
            'nickname': {
                'invalid': '닉네임은 10글자 이내의 한글,영문,숫자,특수기호(_, -)만 가능합니다! (공백 X)',
                'unique' : '이미 존재하는 닉네임입니다!',
                'max_length' : '닉네임은 최대 10글자입니다!',
                'required' : '닉네임을 입력해주세요!'
            },
            'to_open': {
                'invalid_choice': '잘못된 선택입니다!'
            },
            'email' : {
                'invalid': '이메일 형식으로 적어주세요!'
            },
            'github': {
                'invalid': 'Github 주소는 URL 형식으로 입력해주세요!'
            }
        }

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'github', 'email', 'type', 'status', 'self_intro', 'to_open']
        # fields = ['image', 'github', 'email', 'type', 'status', 'to_open']
        error_messages = {
            'email': {
                'invalid': '이메일 형식으로 적어주세요!'
            },
            'github': {
                'invalid': 'Github 주소는 URL 형식으로 입력해주세요!'
            },
            'status': {
                'invalid_choice': '잘못된 선택입니다!'
            },
            'type': {
                'invalid_choice': '잘못된 선택입니다!'
            },
            'to_open': {
                'invalid_choice': '잘못된 선택입니다!'
            }
        }

class ResetNicknameForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname']
        error_messages = {
            'nickname': {
                'invalid': '닉네임은 10글자 이내의 한글,영문,숫자,특수기호(_, -)만 가능합니다! (공백 X)',
                'unique' : '이미 존재하는 닉네임입니다!',
                'max_length' : '닉네임은 최대 10글자입니다!',
                'required' : '닉네임을 입력해주세요!'
            }
        }   

class ActivityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.num = kwargs.pop('num', 0)
        self.instance = kwargs.pop('instance', None)
        self.is_empty = False
        super().__init__(*args, **kwargs)

        for i in range(self.num):
            activity_name = 'activity-name_%s' % (i,)
            activity_type = 'activity-type_%s' % (i,)
            activity_role = 'activity-role_%s' % (i,)
            activity_description = 'activity-description_%s' % (i,)
            activity_start_year = 'activity-start-year_%s' % (i,)
            activity_start_month = 'activity-start-month_%s' % (i,)
            activity_end_year = 'activity-end-year_%s' % (i,)
            activity_end_month = 'activity-end-month_%s' % (i,)

            self.fields[activity_name] = forms.CharField(required=False)
            self.fields[activity_type] = forms.CharField(required=False)
            self.fields[activity_role] = forms.CharField(required=False)
            self.fields[activity_description] = forms.CharField(required=False)
            self.fields[activity_start_year] = forms.CharField(required=False)
            self.fields[activity_start_month] = forms.CharField(required=False)
            self.fields[activity_end_year] = forms.CharField(required=False)
            self.fields[activity_end_month] = forms.CharField(required=False)

    def clean(self):
        activites = []
        i = 0
        activity_name = 'activity-name_%s' % (i ,)
        activity_type = 'activity-type_%s' % (i,)
        activity_role = 'activity-role_%s' % (i,)
        activity_description = 'activity-description_%s' % (i,)
        activity_start_year = 'activity-start-year_%s' % (i,)
        activity_start_month = 'activity-start-month_%s' % (i,)
        activity_end_year = 'activity-end-year_%s' % (i,)
        activity_end_month = 'activity-end-month_%s' % (i,)

        for i in range(self.num):
            name = self.cleaned_data[activity_name]
            type = self.cleaned_data[activity_type]
            role = self.cleaned_data[activity_role]
            description = self.cleaned_data[activity_description]
            start_date = self.cleaned_data[activity_start_year] + "-" + self.cleaned_data[activity_start_month] + "-01"
            end_date = self.cleaned_data[activity_end_year] + "-" + self.cleaned_data[activity_end_month] + "-01"

            if name == "" or type == "" or role == "":
                self.is_empty = True
            else:
                try:
                    datetime.strptime(start_date, date_format)
                except ValueError:
                    start_date = None
                try:
                    datetime.strptime(end_date, date_format)
                except ValueError:
                    end_date = None

                temp_dict = {'name': name, 'type': type, 'role': role, 'description': description,
                             'start_date': start_date, 'end_date': end_date}

                activites.append(temp_dict)
            i += 1

            activity_name = 'activity-name_%s' % (i,)
            activity_type = 'activity-type_%s' % (i,)
            activity_role = 'activity-role_%s' % (i,)
            activity_description = 'activity-description_%s' % (i,)
            activity_start_year = 'activity-start-year_%s' % (i,)
            activity_start_month = 'activity-start-month_%s' % (i,)
            activity_end_year = 'activity-end-year_%s' % (i,)
            activity_end_month = 'activity-end-month_%s' % (i,)

        self.cleaned_data["activity"] = activites

    def save(self):
        profile = self.instance
        profile.activity.all().delete()
        for obj in self.cleaned_data["activity"]:
            temp_activity = Activity(profile=profile, name=obj['name'], type=obj['type'],start_date=obj['start_date'],
                                     end_date=obj['end_date'], description=obj['description'],role=obj['role'])
            try:
                temp_activity.full_clean()
            except ValidationError as e:
                # print('error Activity', e)
                pass
            else:
                temp_activity.save()


class AwardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.num = kwargs.pop('num', 0)
        self.instance = kwargs.pop('instance', None)
        self.is_empty = False
        super().__init__(*args, **kwargs)

        for i in range(self.num):
            award_name = 'award-name_%s' % (i,)
            award_result = 'award-result_%s' % (i,)
            award_description = 'award-description_%s' % (i,)
            award_organization = 'award-organization_%s' % (i,)
            award_year = 'award-year_%s' % (i,)
            award_month = 'award-month_%s' % (i,)

            self.fields[award_name] = forms.CharField(required=False)
            self.fields[award_result] = forms.CharField(required=False)
            self.fields[award_description] = forms.CharField(required=False)
            self.fields[award_organization] = forms.CharField(required=False)
            self.fields[award_year] = forms.CharField(required=False)
            self.fields[award_month] = forms.CharField(required=False)

    def clean(self):
        awards = []
        i = 0
        award_name = 'award-name_%s' % (i,)
        award_result = 'award-result_%s' % (i,)
        award_description = 'award-description_%s' % (i,)
        award_organization = 'award-organization_%s' % (i,)
        award_year = 'award-year_%s' % (i,)
        award_month = 'award-month_%s' % (i,)

        for i in range(self.num):
            name = self.cleaned_data[award_name]
            result = self.cleaned_data[award_result]
            description = self.cleaned_data[award_description]
            organization = self.cleaned_data[award_organization]
            date = self.cleaned_data[award_year] + "-" + self.cleaned_data[award_month] + "-01"

            if name == "" or result == "" :
                self.is_empty = True

            else:
                try:
                    datetime.strptime(date, date_format)
                except ValueError:
                    date = None
                temp_dict = {'name': name, 'result': result, 'description': description,
                             'organization': organization, 'date': date}

                awards.append(temp_dict)
            i += 1

            award_name = 'award-name_%s' % (i,)
            award_result = 'award-result_%s' % (i,)
            award_description = 'award-description_%s' % (i,)
            award_organization = 'award-organization_%s' % (i,)
            award_year = 'award-year_%s' % (i,)
            award_month = 'award-month_%s' % (i,)

        self.cleaned_data["award"] = awards

    def save(self):
        profile = self.instance
        profile.award.all().delete()
        for obj in self.cleaned_data["award"]:
            temp_award = Award(profile=profile, name=obj['name'], result=obj['result'],
                               description=obj['description'],organization=obj['organization'], date=obj['date'])
            try:
                temp_award.full_clean()
            except ValidationError as e:
                # print('error Award', e)
                pass
            else:
                temp_award.save()


class InternForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.num = kwargs.pop('num', 0)
        self.instance = kwargs.pop('instance', None)
        self.is_empty = False
        super().__init__(*args, **kwargs)

        for i in range(self.num):
            intern_name = 'intern-name_%s' % (i,)
            intern_role = 'intern-role_%s' % (i,)
            intern_description = 'intern-description_%s' % (i,)
            intern_start_year = 'intern-start-year_%s' % (i,)
            intern_start_month = 'intern-start-month_%s' % (i,)
            intern_end_year = 'intern-end-year_%s' % (i,)
            intern_end_month = 'intern-end-month_%s' % (i,)

            self.fields[intern_name] = forms.CharField(required=False)
            self.fields[intern_role] = forms.CharField(required=False)
            self.fields[intern_description] = forms.CharField(required=False)
            self.fields[intern_start_year] = forms.CharField(required=False)
            self.fields[intern_start_month] = forms.CharField(required=False)
            self.fields[intern_end_year] = forms.CharField(required=False)
            self.fields[intern_end_month] = forms.CharField(required=False)

    def clean(self):
        interns = []
        i = 0
        intern_name = 'intern-name_%s' % (i,)
        intern_role = 'intern-role_%s' % (i,)
        intern_description = 'intern-description_%s' % (i,)
        intern_start_year = 'intern-start-year_%s' % (i,)
        intern_start_month = 'intern-start-month_%s' % (i,)
        intern_end_year = 'intern-end-year_%s' % (i,)
        intern_end_month = 'intern-end-month_%s' % (i,)

        for i in range(self.num):
            name = self.cleaned_data[intern_name]
            role = self.cleaned_data[intern_role]
            description = self.cleaned_data[intern_description]
            start_date = self.cleaned_data[intern_start_year] + "-" + self.cleaned_data[intern_start_month] + "-01"
            end_date = self.cleaned_data[intern_end_year] + "-" + self.cleaned_data[intern_end_month] + "-01"

            if name == "" or role == "":
                self.is_empty = True

            else:

                try:
                    datetime.strptime(start_date, date_format)
                except ValueError:
                    start_date = None
                try:
                    datetime.strptime(end_date, date_format)
                except ValueError:
                    end_date = None

                temp_dict = {'name': name, 'role': role, 'description': description,
                             'start_date': start_date, 'end_date': end_date}

                interns.append(temp_dict)
            i += 1

            intern_name = 'intern-name_%s' % (i,)
            intern_role = 'intern-role_%s' % (i,)
            intern_description = 'intern-description_%s' % (i,)
            intern_start_year = 'intern-start-year_%s' % (i,)
            intern_start_month = 'intern-start-month_%s' % (i,)
            intern_end_year = 'intern-end-year_%s' % (i,)
            intern_end_month = 'intern-end-month_%s' % (i,)

        self.cleaned_data["intern"] = interns

    def save(self):
        profile = self.instance
        profile.intern.all().delete()
        for obj in self.cleaned_data["intern"]:
            temp_intern = Intern(profile=profile, name=obj['name'], role=obj['role'],
                                 description=obj['description'],start_date=obj['start_date'],end_date=obj['end_date'])
            try:
                temp_intern.full_clean()
            except ValidationError as e:
                # print('error Intern', e)
                pass
            else:
                temp_intern.save()


class LanguageForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.num = kwargs.pop('num', 0)
        self.instance = kwargs.pop('instance', None)
        self.is_empty = False
        super().__init__(*args, **kwargs)

        for i in range(self.num):
            language_name = 'language-name_%s' % (i,)
            language_ability = 'language-ability_%s' % (i,)

            self.fields[language_name] = forms.CharField(required=False)
            self.fields[language_ability] = forms.CharField(required=False)

    def clean(self):
        languages = []
        i = 0
        language_name = 'language-name_%s' % (i,)
        language_ability = 'language-ability_%s' % (i,)

        for i in range(self.num):
            name = self.cleaned_data[language_name]
            ability = self.cleaned_data[language_ability]

            if name == "" or ability == "":
                self.is_empty = True

            else:
                temp_dict = {'name': name, 'ability': ability}

                languages.append(temp_dict)
            i += 1

            language_name = 'language-name_%s' % (i,)
            language_ability = 'language-ability_%s' % (i,)

        self.cleaned_data["language"] = languages

    def save(self):
        profile = self.instance
        profile.language.all().delete()
        for obj in self.cleaned_data["language"]:
            temp_language = Language(profile=profile, name=obj['name'], ability=obj['ability'])
            try:
                temp_language.full_clean()
            except ValidationError as e:
                # print('error Langauge', e)
                pass
            else:
                temp_language.save()


class CertificateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.num = kwargs.pop('num', 0)
        self.instance = kwargs.pop('instance', None)
        self.is_empty = False
        super().__init__(*args, **kwargs)

        for i in range(self.num):
            certificate_name = 'certificate-name_%s' % (i,)
            certificate_year = 'certificate-year_%s' % (i,)
            certificate_month = 'certificate-month_%s' % (i,)

            self.fields[certificate_name] = forms.CharField(required=False)
            self.fields[certificate_year] = forms.CharField(required=False)
            self.fields[certificate_month] = forms.CharField(required=False)

    def clean(self):
        certificates = []
        i = 0
        certificate_name = 'certificate-name_%s' % (i,)
        certificate_year = 'certificate-year_%s' % (i,)
        certificate_month = 'certificate-month_%s' % (i,)

        for i in range(self.num):
            name = self.cleaned_data[certificate_name]
            date = self.cleaned_data[certificate_year] + "-" + self.cleaned_data[certificate_month] + "-01"

            if name == "" or date == "":
                self.is_empty = True

            else:
                try:
                    datetime.strptime(date, date_format)
                except ValueError:
                    date = None

                temp_dict = {'name': name, 'date': date}

                certificates.append(temp_dict)
            i += 1

            certificate_name = 'certificate-name_%s' % (i,)
            certificate_year = 'certificate-year_%s' % (i,)
            certificate_month = 'certificate-month_%s' % (i,)

        self.cleaned_data["certificate"] = certificates

    def save(self):
        profile = self.instance
        profile.certificate.all().delete()
        for obj in self.cleaned_data["certificate"]:
            temp_certificate = Certificate(profile=profile, name=obj['name'], date=obj['date'])
            try:
                temp_certificate.full_clean()
            except ValidationError as e:
                # print('error Certificate', e)
                pass
            else:
                temp_certificate.save()


