# ════════════════════════════════════════════════════════════════
# views.py — Handles only HTTP request/response logic
# All DB operations are delegated to queries.py
# ════════════════════════════════════════════════════════════════

from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .decorators import admin_required
from accounts.models import Main_menuss
from . import queries


# ════════════════════════════════════════
# FUNCTION 1 — HOME PAGE
# Simply renders the homepage with page title and description.
# No database calls needed.
# ════════════════════════════════════════
def home(request):
    context = {
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Brandway helps businesses grow with digital marketing...",
    }
    return render(request, "frontend/index.html", context)


# ════════════════════════════════════════
# FUNCTION 2 — ABOUT PAGE
# Simply renders the About page with page title and description.
# No database calls needed.
# ════════════════════════════════════════
def about(request):
    context = {
        "page_title": "About Brandway - Digital Marketing & Branding Agency",
        "page_description": "Learn about Brandway...",
    }
    return render(request, "frontend/about.html", context)


# ════════════════════════════════════════
# FUNCTION 3 — BLOG LISTING PAGE
# Fetches all active/published blogs from DB and shows them on the blog page.
# ════════════════════════════════════════
def blog(request):
    context = {
        "page_title": "Brandway Blog - Digital Marketing, SEO...",
        "page_description": "Explore the Brandway Blog...",
        "blogs": queries.get_active_blogs(),
    }
    return render(request, "frontend/blog.html", context)


# ════════════════════════════════════════
# FUNCTION 4 — CONTACT PAGE
# GET  → shows the empty contact form.
# POST → validates all 4 fields, saves to DB, shows success message.
# ════════════════════════════════════════
def contact(request):
    if request.method == "POST":

        name = (request.POST.get("name") or "").strip()
        phone = (request.POST.get("phone") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message = (request.POST.get("message") or "").strip()

        if not name or not phone or not email or not message:
            messages.error(request, "All fields are required")
            return redirect("contact")

        queries.contact_save(name, phone, email, message)

        messages.success(request, "Your message has been sent successfully!")

        return redirect("contact")

    context = {
        "page_title": "Contact Brandway...",
        "page_description": "Get in touch with Brandway...",
    }

    return render(request, "frontend/contact.html", context)


# ════════════════════════════════════════
# FUNCTION 5 — SERVICES PAGE
# Fetches a parent menu item by ID from URL, then fetches all its
# active child services ordered by position, and renders both.
# Shows 404 if parent menu ID does not exist.
# ════════════════════════════════════════
def service(request, id):

    services = queries.get_services_by_menu_id(id)

    context = {
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Discover our services",
        "services": services,
    }

    return render(request, "frontend/services.html", context)


# ════════════════════════════════════════
# FUNCTION 6 — SERVICE DETAILS PAGE
# Static page render only. No dynamic data fetched yet.
# ════════════════════════════════════════
def service_details(request, slug):
    service = queries.get_service_by_slug(slug)

    if not service:
        raise Http404("Service not found")

    context = {
        # "page_title": f"{service.title} - Brandway",
        # "page_description": strip_tags(service.content)[:150] if service.content else "Learn more about our specific service offerings at Brandway...",
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Discover our services",
        "service": service,
    }
    return render(request, "frontend/services-details.html", context)


# ════════════════════════════════════════
# FUNCTION 6B — BLOG DETAIL PAGE
# Fetches a single blog post by slug from URL.
# Shows 404 if slug does not match any active blog.
# ════════════════════════════════════════
def blog_details(request, slug):
    blog = get_object_or_404(queries.get_active_blogs(), slug=slug)

    context = {
        "page_title": f"{blog.title} - Brandway Blog",
        "page_description": blog.content[:150],
        "blog": blog,
    }

    return render(request, "frontend/blog-details.html", context)


# ════════════════════════════════════════
# FUNCTION 7 — ADMIN LOGIN
# GET  → shows the login form.
# POST → checks email & password against DB. If valid, saves admin
#        info into session and redirects to dashboard. If wrong, shows error.
# ════════════════════════════════════════
def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = queries.get_admin_by_credentials(email, password)

        if user:
            request.session["admin_id"] = user[0]
            request.session["admin_name"] = user[1]
            request.session["admin_role"] = user[3]
            return redirect("my_admin")
        else:
            messages.error(request, "Invalid login details")

    return render(request, "Backend/auth-login.html")


# ════════════════════════════════════════
# FUNCTION 8 — ADMIN DASHBOARD
# Protected by @admin_required — redirects to login if not logged in.
# Simply renders the admin dashboard page.
# ════════════════════════════════════════
@admin_required
def my_admin(request):
    return render(request, "Backend/index.html")


# ════════════════════════════════════════
# FUNCTION 9 — MENU MANAGER (Admin)
# Protected by @admin_required.
# GET  → fetches all menus from DB and shows menu list.
# POST → reads 4 form fields, saves new menu item to DB via queries.py.
# ════════════════════════════════════════
@admin_required
def menu(request):
    if request.method == "POST":
        queries.create_menu(
            menu_name=request.POST.get("menu_name"),
            menu_link=request.POST.get("menu_link"),
            parent_id=request.POST.get("parent"),
            position=request.POST.get("position"),
        )
        messages.success(request, "Menu saved successfully")
        return redirect("menu")

    return render(request, "Backend/menu.html", {"menus": queries.get_all_menus()})


# ════════════════════════════════════════
# FUNCTION 10 — EDIT MENU (Admin)
# Fetches menu item by ID from URL (404 if not found).
# POST → passes updated form fields to queries.py to save changes.
# Only triggered via modal form — no separate edit page.
# ════════════════════════════════════════
def edit_menu(request, id):
    menu_obj = get_object_or_404(Main_menuss, id=id)

    if request.method == "POST":
        queries.update_menu(
            menu_obj=menu_obj,
            menu_name=request.POST.get("menu_name"),
            menu_link=request.POST.get("menu_link"),
            parent_id=request.POST.get("parent"),
            position=request.POST.get("position"),
        )
        messages.success(request, "Menu updated successfully")
        return redirect("menu")

    return redirect("menu")


# ════════════════════════════════════════
# FUNCTION 11 — DELETE MENU (Admin)
# Fetches menu item by ID from URL (404 if not found).
# Deletes it from DB via queries.py and redirects back to menu list.
# ════════════════════════════════════════
def delete_menu(request, id):
    menu_obj = get_object_or_404(Main_menuss, id=id)

    queries.delete_menu_by_obj(menu_obj)

    messages.success(request, "Menu deleted successfully")
    return redirect("menu")


# ════════════════════════════════════════
# FUNCTION 12 — BLOG SAVE / DELETE (Admin)
# Protected by @admin_required. Handles 3 cases in one function:
# DELETE → if delete_id present in POST, deletes that blog.
# UPDATE → if blog_id present in POST, updates that existing blog.
# CREATE → if no blog_id, creates a brand new blog post.
# GET    → shows blog management page with all blogs listed.
# ════════════════════════════════════════
@admin_required
def blogsave(request):
    if request.method == "POST":
        delete_id = request.POST.get("delete_id")

        if delete_id:
            blog_obj = queries.get_blog_by_id(delete_id)
            if blog_obj:
                queries.delete_blog_by_obj(blog_obj)
                messages.success(request, "Blog deleted successfully")
            else:
                messages.error(request, "Blog not found")
            return redirect("blog-save")

        blog_id = request.POST.get("blog_id")
        title = (request.POST.get("blog_title") or "").strip()
        slug = (request.POST.get("slug") or "").strip()
        content = (request.POST.get("blog_description") or "").strip()
        image = request.FILES.get("blog_image")
        status = int(request.POST.get("blog_status") or 0)

        if not title or not content:
            messages.error(request, "Blog title and description are required")
            return redirect("blog-save")

        if blog_id:
            blog_obj = queries.get_blog_by_id(blog_id)
            if not blog_obj:
                messages.error(request, "Blog not found")
                return redirect("blog-save")

            queries.update_blog(blog_obj, title, slug, image, content, status)
            messages.success(request, "Blog updated successfully")
        else:
            queries.create_blog(title, slug, image, content, status)
            messages.success(request, "Blog saved successfully")

        return redirect("blog-save")

    return render(request, "Backend/blog-save.html", {"blogs": queries.get_all_blogs()})


# ════════════════════════════════════════
# FUNCTION 13 — CONTACT QUERIES (Admin)
# Protected by @admin_required.
# Fetches all contact form submissions from DB and displays them in admin panel.
# ════════════════════════════════════════
@admin_required
def contact_queries(request):
    return render(
        request,
        "Backend/contact-queries.html",
        {"contacts": queries.get_all_contacts()},
    )


@admin_required
def manage_services(request):
    if request.method == "POST":
        if "delete_id" in request.POST:
            queries.delete_service(request.POST.get("delete_id"))
            messages.success(request, "Service deleted successfully.")
            return redirect("manage_services")

        service_id = request.POST.get("service_id")
        title = request.POST.get("service_title")
        slug = request.POST.get("slug")
        parent_menu_id = request.POST.get("parent_menu_id")
        content = request.POST.get("service_description")
        status = request.POST.get("service_status")
        image_file = request.FILES.get("service_image")  # raw file, ORM handles saving

        if service_id:
            queries.update_service(
                service_id, title, slug, parent_menu_id, content, status, image_file
            )
            messages.success(request, "Service updated successfully.")
        else:
            queries.insert_service(
                title, slug, parent_menu_id, image_file, content, status
            )
            messages.success(request, "Service added successfully.")

        return redirect("manage_services")

    services = queries.get_all_services()
    menus = queries.get_all_menus()
    context = {"services": services, "menus": menus}
    return render(request, "Backend/service-save.html", context)
