from bootstrap_daterangepicker.fields import DateRangeField
from bootstrap_daterangepicker.widgets import DateRangeWidget
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.utils import timezone

from backend.models import Profile, Activity, ActivityType


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
    parse_activities = forms.BooleanField(required=False)

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
            'parse_activities',
            Div(
                Submit('submit', 'Save'),
                css_class='offset-lg-2',
            ),
        )


class ActivityForm(forms.ModelForm):
    duration = forms.TimeField(widget=forms.TimeInput(format='%H:%M:%S'))

    class Meta:
        model = Activity
        fields = [
            'description',
            'activity_type',
            'date',
            'distance_meters',
            'total_elevation_gain',
            'avg_heart_rate',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            'description',
            'activity_type',
            'date',
            'duration',
            'distance_meters',
            'total_elevation_gain',
            'avg_heart_rate',
            Div(
                Submit('submit', 'Save'),
                css_class='offset-lg-2',
            ),
        )

        self.fields['date'].widget = forms.DateInput(attrs={'class': 'datepicker'})


class DataSelectForm(forms.Form):
    date_range = DateRangeField(
        input_formats=['%d/%m/%Y'],
        widget=DateRangeWidget(
            format='%d/%m/%Y',
        )
    )
    activity_type = forms.ModelMultipleChoiceField(queryset=ActivityType.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Div(
                Div(
                    'activity_type',
                    css_class='col-lg-12',
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'date_range',
                    css_class='col-lg-12',
                ),
                css_class='row',
            ),
            Div(
                Submit('submit', 'Run'),
                css_class='',
            ),
        )
        now = timezone.now()
        now_minus_month = now - relativedelta(months=1)
        self.fields['date_range'].widget.picker_options = {
            'startDate': now_minus_month.strftime('%d/%m/%Y'),
            'maxDate': now.strftime('%d/%m/%Y'),
        }


class GraphSelectForm(DataSelectForm):
    data_points = forms.MultipleChoiceField(choices=[('Pace', 'Pace'), ('Duration', 'Duration')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_main_form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.layout = Layout(
            Div(
                Div(
                    'activity_type',
                    css_class='col-lg-6',
                ),
                Div(
                    'data_points',
                    css_class='col-lg-6',
                ),
                css_class='row',
            ),
            Div(
                Div(
                    'date_range',
                    css_class='col-lg-12',
                ),
                css_class='row',
            ),
            Div(
                Submit('submit', 'Run'),
                css_class='',
            ),
        )
        now = timezone.now()
        now_minus_month = now - relativedelta(months=1)
        self.fields['date_range'].widget.picker_options = {
            'startDate': now_minus_month.strftime('%d/%m/%Y'),
            'maxDate': now.strftime('%d/%m/%Y'),
        }
