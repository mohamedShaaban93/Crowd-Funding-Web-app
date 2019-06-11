from django.urls import path, re_path
from .views import *
app_name = "users"
urlpatterns = [
   path("profile/<int:uid>", profile, name="profile"),
   path("delete", deleteAccount, name="delete"),
   path("edit/<int:uid>", editprofile, name="edit"),
   path("logout", logout_view , name="logout"),
   path("login", loginuser, name="login2"),
   path("register", register2 ,name="register"),
   re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
           activate, name='activate')

]
