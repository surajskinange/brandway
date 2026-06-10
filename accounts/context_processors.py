from .models import Main_menuss

def menu_context(request):
    menus = Main_menuss.objects.filter(
        parent__isnull=True,
        is_active=True
    ).order_by("position")

    return {
        'menus': menus
    }