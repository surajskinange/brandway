from django.contrib import admin
from django.urls import path
from .views import home, about, blog, contact, admin_login, menu, my_admin, edit_menu, delete_menu

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("home/", home, name="home"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("contact/", contact, name="contact"),
    path("my-admin/", my_admin, name="my_admin"),
    # AUTH
    path("login/", admin_login, name="admin_login"),
    # DASHBOARD
    path("dashboard/", my_admin, name="dashboard"),
    # MENU
    path("menu/", menu, name="menu"),
    path("menu/edit/<int:id>/", edit_menu, name="edit_menu"),
    path("menu/delete/<int:id>/", delete_menu, name="delete_menu"),
]