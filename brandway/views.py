from django.shortcuts import render


def home(request):
    context = {
        "page_title": "Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Brandway helps businesses grow with digital marketing, SEO, branding, website development, Shopify solutions, and performance-driven strategies.",
    }
    return render(request, "index.html", context)


def about(request):
    context = {
        "page_title": "About Brandway - Digital Marketing & Branding Agency",
        "page_description": "Learn about Brandway, our digital marketing, branding, web design, and Shopify development services for startups and growing businesses.",
    }
    return render(request, "about.html", context)


def blog(request):
    context = {
        "page_title": "Brandway Blog - Digital Marketing, SEO, Branding & Web Design Insights",
        "page_description": "Explore the Brandway Blog for expert insights on digital marketing, SEO, branding, web design, Shopify development, and performance-driven strategies.",
    }
    return render(request, "blog.html", context)


def contact(request):
    context = {
        "page_title": "Contact Brandway - Digital Marketing, Branding & Web Solutions",
        "page_description": "Get in touch with Brandway for digital marketing, SEO, branding, web design, Shopify development, and performance-driven solutions for your business.",
    }
    return render(request, "contact.html", context)


# def about(request):
#     return render(request, 'about.html')
