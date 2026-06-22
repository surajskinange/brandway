# ════════════════════════════════════════════════════════════════
# queries.py — All database queries and save operations
# Import this in views.py to keep views clean and focused
# ════════════════════════════════════════════════════════════════

from django.db import connection
from django.db.models import Prefetch
from django.utils.text import slugify

from accounts.models import Main_menuss, Service, Blog, Contact

# ════════════════════════════════════════
# ADMIN QUERIES
# ════════════════════════════════════════


def get_admin_by_credentials(email, password):
    """Fetch a single active admin by matching email and password."""
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, email, role
            FROM admin_users
            WHERE email=%s AND password=%s AND is_active=true
            """,
            [email, password],
        )
        return cursor.fetchone()


# ════════════════════════════════════════
# MENU QUERIES
# ════════════════════════════════════════


def get_all_menus():
    """Return all menu items."""
    return Main_menuss.objects.all()


def get_parent_obj(parent_id):
    """Safely fetch a parent menu object by ID."""
    if parent_id and str(parent_id).strip().isdigit():
        return Main_menuss.objects.filter(id=parent_id).first()
    return None


def create_menu(menu_name, menu_link, parent_id, position, submenu=""):
    """Create and save a new menu item."""
    parent_obj = get_parent_obj(parent_id)
    return Main_menuss.objects.create(
        menu_name=menu_name,
        menu_link=menu_link,
        submenu=submenu,
        parent=parent_obj,
        position=position or 1,
    )


def update_menu(menu_obj, menu_name, menu_link, parent_id, position, submenu=""):
    """Update an existing menu item and save it."""
    menu_obj.menu_name = menu_name
    menu_obj.menu_link = menu_link
    menu_obj.submenu = submenu
    menu_obj.parent = get_parent_obj(parent_id)
    menu_obj.position = (
        int(position) if position and str(position).strip().isdigit() else 1
    )
    menu_obj.save()
    return menu_obj


def delete_menu_by_obj(menu_obj):
    """Delete the given menu object."""
    menu_obj.delete()


def get_menus_with_services():
    """Get top-level active menus with their child menus and services prefetched."""
    return Main_menuss.objects.filter(
        parent_id=None,
        is_active=1,
    ).prefetch_related(
        "main_menuss_set",
        "service_set",
    )


# ════════════════════════════════════════
# BLOG QUERIES
# ════════════════════════════════════════


def get_all_blogs():
    """Return all blog posts for the admin blog list."""
    return Blog.objects.all()


def get_active_blogs():
    """Return active blog posts for the frontend blog page."""
    return Blog.objects.filter(status=1)


def get_blog_by_id(blog_id):
    """Safely fetch a blog by ID."""
    if blog_id and str(blog_id).strip().isdigit():
        return Blog.objects.filter(id=blog_id).first()
    return None


def unique_blog_slug(title, slug=None, blog_id=None):
    """Build a unique slug for a blog, excluding the current blog while editing."""
    base_slug = slugify(slug or title) or "blog"
    unique_slug = base_slug
    counter = 1

    while Blog.objects.filter(slug=unique_slug).exclude(id=blog_id).exists():
        counter += 1
        unique_slug = f"{base_slug}-{counter}"

    return unique_slug


def create_blog(title, slug, image, content, status):
    """Create and save a new blog post."""
    return Blog.objects.create(
        title=title,
        slug=unique_blog_slug(title, slug),
        image=image,
        content=content,
        status=status,
    )


def update_blog(blog_obj, title, slug, image, content, status):
    """Update an existing blog post. Keeps old image if no new image sent."""
    blog_obj.title = title
    blog_obj.slug = unique_blog_slug(title, slug, blog_obj.id)
    blog_obj.content = content
    blog_obj.status = status

    if image:
        blog_obj.image = image

    blog_obj.save()
    return blog_obj


def delete_blog_by_obj(blog_obj):
    """Delete the given blog post."""
    blog_obj.delete()


# ════════════════════════════════════════
# CONTACT QUERIES
# ════════════════════════════════════════


def contact_save(name, phone, email, message):
    """Save a new contact message."""
    return Contact.objects.create(name=name, phone=phone, email=email, message=message)


def get_all_contacts():
    """Return all contact inquiries for the admin list."""
    return Contact.objects.all().order_by("-created_at")


# ════════════════════════════════════════
# SERVICE QUERIES
# ════════════════════════════════════════


def get_all_services():
    """Get all non-deleted services."""
    return Service.objects.filter(is_deleted=False).order_by("-created_at")


def get_service_by_id(service_id):
    """Fetch a single non-deleted service by ID."""
    try:
        return Service.objects.get(id=service_id, is_deleted=False)
    except Service.DoesNotExist:
        return None


def get_service_by_slug(slug):
    """Fetch a single active, non-deleted service by slug."""
    return Service.objects.filter(slug=slug, status=True, is_deleted=False).first()


def get_services_by_menu_id(menu_id):
    """Get active services under a given menu, ordered by title."""
    return Service.objects.filter(
        parent_menu_id=menu_id, is_deleted=False, status=1
    ).order_by("title")


# ════════════════════════════════════════
# SERVICE INSERT QUERIES
# ════════════════════════════════════════


def insert_service(title, slug, parent_menu_id, image_file, content, status):
    """Create a new service."""
    return Service.objects.create(
        title=title,
        slug=slug,
        parent_menu_id=parent_menu_id,
        content=content,
        status=status,
        image=image_file,
    )


# ════════════════════════════════════════
# SERVICE UPDATE QUERIES
# ════════════════════════════════════════


def update_service(
    service_id, title, slug, parent_menu_id, content, status, image_file=None
):
    """Update an existing service."""
    service = get_service_by_id(service_id)
    if not service:
        raise ValueError("Service not found")

    service.title = title
    service.slug = slug
    service.parent_menu_id = parent_menu_id
    service.content = content
    service.status = status

    if image_file:
        service.image = image_file

    service.save()
    return service


# ════════════════════════════════════════
# SERVICE QUERIES DELETE
# ════════════════════════════════════════


def delete_service(service_id):
    """Soft delete a service."""
    try:
        service = Service.objects.get(id=service_id)
        service.is_deleted = True
        service.save()
        return True
    except Service.DoesNotExist:
        return False
