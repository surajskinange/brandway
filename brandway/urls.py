from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    blogsave,
    home,
    about,
    blog,
    contact,
    admin_login,
    menu,
    my_admin,
    edit_menu,
    delete_menu,
    service,
    service_details,
    blog_details,
    contact_queries,
)

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
    # SERVICES
    path("services/<int:id>/", service, name="service"),
    path("services-details", service_details, name="service_details"),
    path("blog-save/", blogsave, name="blog-save"),
    path("blog-details/<slug:slug>/", blog_details, name="blog_details"),
    path("contact-queries/", contact_queries, name="contact_queries"), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
