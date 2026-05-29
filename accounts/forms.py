from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from accounts.models import Address, UserProfile

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    """Sign-up form: email + name + password (with confirmation)."""

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Create a password"}),
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Re-enter password"}),
    )

    class Meta:
        model = User
        fields = ["email", "name"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields do not match.")
        validate_password(password2)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class PasswordResetRequestForm(forms.Form):
    """Step 1: user enters the email they want a reset link sent to."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )

    def clean_email(self):
        # Normalize only. We deliberately DON'T error when the email is unknown:
        # revealing which emails have accounts is an enumeration leak. The view
        # shows the same "check your inbox" message either way.
        return self.cleaned_data["email"].lower()


class SetNewPasswordForm(forms.Form):
    """Step 2: user chooses a new password (with confirmation) after clicking
    the emailed link. Not a ModelForm — the view owns which user it applies to."""

    password1 = forms.CharField(
        label="New password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Choose a new password"}),
    )
    password2 = forms.CharField(
        label="Confirm new password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Re-enter new password"}),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields do not match.")
        validate_password(password2)
        return password2


class LoginForm(forms.Form):
    """Collects email + password for authentication (not tied to a model)."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Your password"}),
    )

    def clean_email(self):
        return self.cleaned_data["email"].lower()


# A reusable mixin: loops over every field and adds Bootstrap's "form-control"
# class, so we don't repeat widget attrs on each field below.
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css}".strip()


class UserNameForm(BootstrapFormMixin, forms.ModelForm):
    """Edits the `name` field that lives on the User model itself."""

    class Meta:
        model = User
        fields = ["name"]


class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    """Edits the fields on the related UserProfile row."""

    class Meta:
        model = UserProfile
        fields = ["phone", "avatar", "bio", "date_of_birth"]
        widgets = {
            # type="date" renders the browser's native date picker.
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class AddressForm(BootstrapFormMixin, forms.ModelForm):
    """Create/edit form for a single Address. `user` is set in the view,
    not by the user, so it's deliberately excluded from `fields`."""

    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "address_type",
            "is_default",
        ]
