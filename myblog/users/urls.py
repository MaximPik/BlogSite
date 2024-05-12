from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    # path() для страницы регистрации нового пользователя
    # её полный адрес будет auth/signup/, но префикс auth/ обрабатывется в головном urls.py
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("password_change/", auth_view.PasswordChangeView.as_view(), name="password_change"),
    path("login/", auth_view.LoginView.as_view(), name="login"),
    #path("logout/", auth_view.LogoutView.as_view(http_method_names=["post", "get", "options"]), name="logout"),
    path("logout/", views.logout_view, name="my_logout"),
    path("password_change/done/", auth_view.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("reset/<uidb64>/<token>/", auth_view.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/done/", auth_view.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/done/", auth_view.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]