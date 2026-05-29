from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verify/<uidb64>/<token>/", views.verify_email_view, name="verify_email"),
    path("resend-verification/", views.resend_verification_view, name="resend_verification"),
    # Password reset (request -> done -> confirm -> complete)
    path("password-reset/", views.password_reset_request_view, name="password_reset"),
    path("password-reset/done/", views.password_reset_done_view, name="password_reset_done"),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        views.password_reset_confirm_view,
        name="password_reset_confirm",
    ),
    path("password-reset/complete/", views.password_reset_complete_view, name="password_reset_complete"),
    # Profile
    path("profile/", views.profile_view, name="profile"),
    # Addresses (CRUD). UUID converter matches the Address UUID primary key.
    path("addresses/", views.address_list_view, name="address_list"),
    path("addresses/add/", views.address_add_view, name="address_add"),
    path("addresses/<uuid:pk>/edit/", views.address_edit_view, name="address_edit"),
    path("addresses/<uuid:pk>/delete/", views.address_delete_view, name="address_delete"),
    path("addresses/<uuid:pk>/set-default/", views.address_set_default_view, name="address_set_default"),
]
