from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages


def home(request):
    context = {
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Brandway helps businesses grow with digital marketing, SEO, branding, website development, Shopify solutions, and performance-driven strategies.",
    }
    return render(request, "frontend/index.html", context)


def about(request):
    context = {
        "page_title": "About Brandway - Digital Marketing & Branding Agency",
        "page_description": "Learn about Brandway, our digital marketing, branding, web design, and Shopify development services for startups and growing businesses.",
    }
    return render(request, "frontend/about.html", context)


def blog(request):
    context = {
        "page_title": "Brandway Blog - Digital Marketing, SEO, Branding & Web Design Insights",
        "page_description": "Explore the Brandway Blog for expert insights on digital marketing, SEO, branding, web design, Shopify development, and performance-driven strategies.",
    }
    return render(request, "frontend/blog.html", context)


def contact(request):
    context = {
        "page_title": "Contact Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Get in touch with Brandway for digital marketing, SEO, branding, web design, Shopify development, and performance-driven solutions for your business.",
    }
    return render(request, "frontend/contact.html", context)


# there is stared admin panel for this project. you can access it by going to /my-admin/ url. the template for this admin panel is located in Backend/index.html. you can customize this template as per your needs. the view for this admin panel is defined in views.py file. you can add your logic in this view as per your requirements.
def my_admin(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    return render(request, "Backend/index.html")


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

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
            request.session["admin_id"] = user[0]
            request.session["admin_name"] = user[1]
            request.session["admin_role"] = user[3]

            return redirect("my_admin")  # ✅ FIXED
        else:
            messages.error(request, "Invalid login details")

    return render(request, "Backend/auth-login.html")


def my_admin(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")

    return render(request, "Backend/index.html")


# def about(request):
#     return render(request, 'about.html')
