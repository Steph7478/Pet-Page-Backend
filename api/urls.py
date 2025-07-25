from django.urls import path
from adoption.views.adopt import AdoptionView, ApproveAdoptionView, RejectAdoptionView
from users.views.auth import DeleteAccountView, LoginView, LogoutView, RegisterView
from users.views.refreshToken import refresh_token
from adoption.views.formulario import FormularioView
from pets.views.pet import PetView
from users.views.userInfo import MeView

urlpatterns = [
    path("auth/refresh", refresh_token),
    path("auth/login", LoginView.as_view()),
    path("auth/register", RegisterView.as_view()),
    path("auth/logout", LogoutView.as_view()),
    path("auth/me", MeView.as_view()),
    path('auth/delete-account', DeleteAccountView.as_view()),

    path("formularios", FormularioView.as_view()),
    path("pets", PetView.as_view()),
    path('pets/<uuid:petId>', PetView.as_view()),
    
    path("adoptions", AdoptionView.as_view()),
    path('adoptions/approve', ApproveAdoptionView.as_view()),
    path('adoptions/reject', RejectAdoptionView.as_view()),
]