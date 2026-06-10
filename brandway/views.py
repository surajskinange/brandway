from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from .decorators import admin_required
from accounts.models import Main_menuss
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Main_menuss


# ════════════════════════════════════════
# FUNCTION 1 — HOME PAGE
# ════════════════════════════════════════
def home(request):
    context = {
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Brandway helps businesses grow with digital marketing...",
    }

    return render(request, "frontend/index.html", context)


# ════════════════════════════════════════
# FUNCTION 2 — ABOUT PAGE
# ════════════════════════════════════════
def about(request):
    # START: Sets page title and description for SEO
    context = {
        "page_title": "About Brandway - Digital Marketing & Branding Agency",
        "page_description": "Learn about Brandway...",
    }
    return render(request, "frontend/about.html", context)
    # END: Opens about page template and sends context data to it


# ════════════════════════════════════════
# FUNCTION 3 — BLOG PAGE
# ════════════════════════════════════════
def blog(request):
    # START: Sets page title and description for SEO
    context = {
        "page_title": "Brandway Blog - Digital Marketing, SEO...",
        "page_description": "Explore the Brandway Blog...",
    }
    return render(request, "frontend/blog.html", context)
    # END: Opens blog page template and sends context data to it


# ════════════════════════════════════════
# FUNCTION 4 — CONTACT PAGE
# ════════════════════════════════════════
def contact(request):
    # START: Sets page title and description for SEO
    context = {
        "page_title": "Contact Brandway...",
        "page_description": "Get in touch with Brandway...",
    }
    return render(request, "frontend/contact.html", context)
    # END: Opens contact page template and sends context data to it


# ════════════════════════════════════════
# FUNCTION 5 — ADMIN LOGIN
# ════════════════════════════════════════
def admin_login(request):
    # START: Checks if form was submitted (POST) or page just opened (GET)

    if request.method == "POST":
        # Gets email and password typed by user in login form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Runs SQL query to find matching admin in database
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, email, role 
                FROM admin_users 
                WHERE email=%s AND password=%s AND is_active=true
                """,
                [email, password],
            )
            user = cursor.fetchone()

        if user:
            # Saves admin info in session (keeps admin logged in)
            request.session["admin_id"] = user[0]
            request.session["admin_name"] = user[1]
            request.session["admin_role"] = user[3]
            return redirect("my_admin")
        else:
            # Shows error message if email/password is wrong
            messages.error(request, "Invalid login details")

    return render(request, "Backend/auth-login.html")
    # END: If login ok → goes to dashboard. If wrong → shows error on login page


# ════════════════════════════════════════
# FUNCTION 6 — ADMIN DASHBOARD
# ════════════════════════════════════════
@admin_required
def my_admin(request):
    # START: Checks if admin is logged in (via @admin_required decorator)
    return render(request, "Backend/index.html")
    # END: Opens admin dashboard page


# ════════════════════════════════════════
# FUNCTION 7 — MENU MANAGER
# ════════════════════════════════════════
@admin_required
def menu(request):
    if request.method == "POST":
        menu_name = request.POST.get("menu_name")
        menu_link = request.POST.get("menu_link")
        submenu = request.POST.get("submenu")
        parent_id = request.POST.get("parent")
        position = request.POST.get("position")

        parent_obj = None
        if parent_id and parent_id.strip():
            parent_obj = Main_menuss.objects.filter(id=parent_id).first()

        Main_menuss.objects.create(
            menu_name=menu_name,
            menu_link=menu_link,
            submenu=submenu,
            parent=parent_obj,
            position=position or 1,
        )

        messages.success(request, "Menu saved successfully")
        return redirect("menu")

    return render(request, "Backend/menu.html", {"menus": Main_menuss.objects.all()})


def edit_menu(request, id):
    menu_obj = get_object_or_404(Main_menuss, id=id)
    if request.method == "POST":

        # DEBUG: see exactly what the form is sending
        print("POST DATA:", request.POST)

        menu_obj.menu_name = request.POST.get("menu_name")
        menu_obj.menu_link = request.POST.get("menu_link")
        menu_obj.submenu = request.POST.get("submenu")

        # safe parent handling
        parent_id = request.POST.get("parent")
        if parent_id and parent_id.strip().isdigit():
            menu_obj.parent = Main_menuss.objects.filter(id=parent_id).first()
        else:
            menu_obj.parent = None

        # safe position handling
        position = request.POST.get("position")
        menu_obj.position = (
            int(position) if position and position.strip().isdigit() else 1
        )

        menu_obj.save()
        messages.success(request, "Menu updated successfully")
        return redirect("menu")

    return redirect("menu")


def delete_menu(request, id):
    menu_obj = get_object_or_404(Main_menuss, id=id)
    menu_obj.delete()
    messages.success(request, "Menu deleted successfully")
    return redirect("menu")
