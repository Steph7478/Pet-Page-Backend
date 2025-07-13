from django.urls import path
from adoption.views.allowAdoption import AllowAdoptionView
from users.views.refreshToken import refresh_token
from adoption.views.formulario import FormularioView
from users.views.deleteAccount import DeleteAccountView
from users.views.logout import LogoutView
from users.views.login import LoginView
from pets.views.pet import PetView
from users.views.register import RegisterView
from users.views.userInfo import MeView

urlpatterns = [
    path("auth/refresh", refresh_token),
    path("auth/login", LoginView.as_view()),
    path("auth/register", RegisterView.as_view()),
    path("auth/logout", LogoutView.as_view()),
    path("auth/me", MeView.as_view()),
    path('auth/delete-account', DeleteAccountView.as_view()),

    path("formulario", FormularioView.as_view()),
    path("pets", PetView.as_view()),
    path("adoption", AllowAdoptionView.as_view())
]