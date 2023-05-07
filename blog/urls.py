from django.urls import path

from . import views
urlpatterns = [
    path("" , views.index , name="Home"),
    path("all-posts",views.all_posts , name="posts"),
    path("posts/<slug>", views.post_datails , name = "details"),
    path("register",views.AuthorRegister , name = "register"),
    path("add-new-post",views.addPost),
    path("login",views.LogIn.as_view(), name = "login"),
    path("logout",views.log_out, name = 'logout'),
    path("account" , views.profileSettings.as_view() , name = 'profilesettings')
]
