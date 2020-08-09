from crispy_forms.bootstrap import FormActions
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Submit, Button, ButtonHolder, Div, HTML
from django.urls import reverse_lazy


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
