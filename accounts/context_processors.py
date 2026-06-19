from django.db.models import Prefetch

from .models import Main_menuss

def menu_context(request):
    active_children = Main_menuss.objects.filter(is_active=True).order_by("position")
    menus = Main_menuss.objects.filter(
        parent__isnull=True,
        is_active=True
    ).prefetch_related(
        Prefetch("main_menuss_set", queryset=active_children, to_attr="active_children")
    ).order_by("position")

    return {
        'menus': menus
    }
