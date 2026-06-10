from django.shortcuts import render, redirect
from accounts.models import Main_menuss


def menu(request):
    if request.method == "POST":
        Main_menuss.objects.create(
            menu_name=request.POST.get("menu_name"),
            menu_link=request.POST.get("menu_link"),
            submenu=request.POST.get("submenu"),
            parent_id=request.POST.get("parent") or None,
            position=request.POST.get("position") or 1,
        )

        return redirect("menu")  # apne url name ke according

    menus = Main_menuss.objects.all()
    return render(request, "Backend/menu.html", {"menus": menus})


