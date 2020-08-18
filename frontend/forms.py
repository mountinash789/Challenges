from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy

from backend.models import Profile


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password',
            Div(
                Submit('submit', 'Login'),
                HTML('<a class="btn btn-secondary" href="{}">Register</a>'.format(reverse_lazy('front:register'))),
                HTML('<a href="{}"><img src="/static/images/btn_google_signin_dark_pressed_web.png"/></a>'.format(
                    reverse_lazy('front:social:begin', kwargs={'backend': 'google-oauth2'}))),
                css_class='offset-lg-2',
            ),
        )


class RegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'username',
            'password1',
            'password2',
            Div(
                Submit('submit', 'Register'),
                HTML('Or <a href="{}"><img src="/static/images/btn_google_signin_dark_pressed_web.png"/></a>'.format(
                    reverse_lazy('front:social:begin', kwargs={'backend': 'google-oauth2'}))),
                css_class='offset-lg-2',
            ),
        )


class ProfileForm(forms.ModelForm):
    dob = forms.DateField(required=True, input_formats=['%d/%m/%Y'],
                          widget=forms.DateInput(attrs={'class': 'datepicker'}),
                          label='Date of Birth')

    class Meta:
        model = Profile
        fields = [
            'dob'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            FieldWithButtons(Field('dob', autocomplete="off"),
                             StrictButton('<i class="fa fa-calendar fa-fw"></i>',
                                          css_class='btn-outline-secondary datepicker-btn')),
            Div(
                Submit('submit', 'Save'),
                css_class='offset-lg-2',
            ),
        )
