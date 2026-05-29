from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.http import require_POST

from accounts.emails import send_password_reset_email, send_verification_email
from accounts.forms import (
    AddressForm,
    LoginForm,
    PasswordResetRequestForm,
    ProfileForm,
    RegistrationForm,
    SetNewPasswordForm,
    UserNameForm,
)
from accounts.models import Address
from accounts.tokens import email_verification_token, password_reset_token

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_verification_email(user)
            login(request, user)
            messages.success(
                request,
                "Account created. We've emailed you a verification link — please check your inbox.",
            )
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                return redirect("home")
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")


def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ValidationError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=["is_verified"])
        messages.success(request, "Email verified successfully. Thank you!")
    else:
        messages.error(request, "This verification link is invalid or has expired.")

    return redirect("home")


@require_POST
def resend_verification_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("accounts:login")
    if user.is_verified:
        messages.info(request, "Your email is already verified.")
    else:
        send_verification_email(user)
        messages.success(request, "Verification email sent. Please check your inbox.")
    return redirect("home")


# ---------------------------------------------------------------------------
# Password reset (request -> email -> confirm -> complete)
# ---------------------------------------------------------------------------
def password_reset_request_view(request):
    """Step 1: ask for an email and send a reset link if an account exists."""
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # If no user matches, we silently skip sending — but still redirect
            # to the same "done" page, so an attacker can't tell which emails
            # are registered (account-enumeration defense).
            user = User.objects.filter(email=email, is_active=True).first()
            if user is not None:
                send_password_reset_email(user)
            return redirect("accounts:password_reset_done")
    else:
        form = PasswordResetRequestForm()
    return render(request, "accounts/password_reset_request.html", {"form": form})


def password_reset_done_view(request):
    """Step 1b: static confirmation that an email was (maybe) sent."""
    return render(request, "accounts/password_reset_done.html")


def password_reset_confirm_view(request, uidb64, token):
    """Step 2: validate the emailed link, then let the user set a new password."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ValidationError, User.DoesNotExist):
        user = None

    # Token is invalid/expired (or uid didn't decode to a real user).
    if user is None or not password_reset_token.check_token(user, token):
        messages.error(request, "This password reset link is invalid or has expired.")
        return redirect("accounts:password_reset")

    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.save(update_fields=["password"])
            # Changing the password rotates the hash, so the used token can
            # never be replayed. Send them to log in with the new password.
            return redirect("accounts:password_reset_complete")
    else:
        form = SetNewPasswordForm()
    return render(request, "accounts/password_reset_confirm.html", {"form": form})


def password_reset_complete_view(request):
    """Step 3: tell the user the password was changed and link to login."""
    return render(request, "accounts/password_reset_complete.html")


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------
@login_required
def profile_view(request):
    """Show + edit the logged-in user's name and profile fields together.

    Two forms (User + UserProfile) are bound on the same POST. We validate
    BOTH before saving EITHER, so a half-valid submit doesn't half-save.
    """
    profile = request.user.profile  # created by the post_save signal

    if request.method == "POST":
        # request.FILES is required so the avatar ImageField can receive uploads.
        name_form = UserNameForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if name_form.is_valid() and profile_form.is_valid():
            name_form.save()
            profile_form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        name_form = UserNameForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {"name_form": name_form, "profile_form": profile_form},
    )


# ---------------------------------------------------------------------------
# Addresses (CRUD)
# ---------------------------------------------------------------------------
@login_required
def address_list_view(request):
    # related_name="addresses" on the FK lets us query straight off the user.
    addresses = request.user.addresses.all()
    return render(request, "accounts/address_list.html", {"addresses": addresses})


@login_required
def address_add_view(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)  # build the object, don't hit DB yet
            address.user = request.user         # attach the owner ourselves
            # First address a user adds becomes their default automatically.
            if not request.user.addresses.exists():
                address.is_default = True
            address.save()
            messages.success(request, "Address added.")
            return redirect("accounts:address_list")
    else:
        form = AddressForm()
    return render(request, "accounts/address_form.html", {"form": form, "is_edit": False})


@login_required
def address_edit_view(request, pk):
    # get_object_or_404 with user=request.user ensures users can only edit
    # THEIR OWN addresses — not someone else's by guessing the UUID.
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address updated.")
            return redirect("accounts:address_list")
    else:
        form = AddressForm(instance=address)
    return render(request, "accounts/address_form.html", {"form": form, "is_edit": True})


@login_required
@require_POST
def address_delete_view(request, pk):
    # POST-only: deleting is state-changing, so it must carry a CSRF token
    # and can't be triggered by a stray GET / link prefetch.
    address = get_object_or_404(Address, pk=pk, user=request.user)
    was_default = address.is_default
    address.delete()
    # If we deleted the default, promote the next-newest address to default.
    if was_default:
        next_address = request.user.addresses.first()
        if next_address:
            next_address.is_default = True
            next_address.save()
    messages.success(request, "Address deleted.")
    return redirect("accounts:address_list")


@login_required
@require_POST
def address_set_default_view(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()  # model.save() unsets is_default on the others
    messages.success(request, "Default address updated.")
    return redirect("accounts:address_list")
