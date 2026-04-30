from django import forms
from .models import Employee, LeaveDetail
from datetime import date


class CreateEmployee(forms.Form):
    GENDER_CHOICES = [
        ("Select", "Select"),
        ("Male", "Male"),
        ("Female", "Female"),
    ]
    firstname = forms.CharField(label="First Name", max_length=30, required=True)
    middle_initial = forms.CharField(
        label="Middle Initial(s)", max_length=3, required=False
    )
    lastname = forms.CharField(label="Last Name", max_length=30, required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    # ethnicity = forms.CharField(max_length=50, blank=True, null=True)
    # race = forms.CharField(max_length=50, blank=True, null=True)
    nationality = forms.CharField(max_length=50, required=True)
    # preferred_name = forms.CharField(max_length=50, blank=True, null=True)
    pronouns = forms.CharField(max_length=10, required=False)
    birth_date = forms.DateField(required=True)
    street_address = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=50, required=True)
    state = forms.CharField(max_length=50, required=False)
    # province = forms.CharField(max_length=50, blank=True, null=True)
    zipcode = forms.CharField(max_length=20, required=True)
    country = forms.CharField(max_length=50, required=True)
    # government_id = forms.CharField(max_length=50, blank=True, null=True)
    phone_number = forms.CharField(max_length=20, required=True)
    social_security_number = forms.CharField(max_length=20, required=False)
    personal_email = forms.EmailField(required=True)
    # emergency_contact_name = forms.CharField(max_length=50, blank=True, null=True)
    # emergency_contact_phone = forms.CharField(max_length=20, blank=True, null=True)
    hire_date = forms.DateField(required=True)


class CreateEmpFromModel(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"
        exclude = ["id", "user", "employment_end_date", "last_promotion_date"]


class RequestLeave(forms.ModelForm):
    class Meta:
        model = LeaveDetail
        fields = ["leave_type", "start_date", "end_date", "message"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4, "maxlength": 500}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        errors = []

        if start_date and (start_date < date.today()):
            errors.append("Start date cannot be in the past.")
        if (start_date and end_date) and (start_date > end_date):
            errors.append("Start date must be before end date.")
        if errors:
            raise forms.ValidationError(errors)
        return cleaned_data
