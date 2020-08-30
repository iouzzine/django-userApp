from django.urls import path
from pages.views import Index, Register, Dashboard, Logout

urlpatterns = [
    path('', Index.as_view(), name="index"),
    path('register/', Register.as_view(), name="register"),
    path('dashboard/', Dashboard.as_view(), name="dashboard"),
    path('logout/', Logout.as_view(), name="logout")
]
