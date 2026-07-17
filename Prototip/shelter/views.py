from django.shortcuts import get_object_or_404, redirect, render

from .models import Animal, FosterRequest


def ensure_seed_data():
    animal_names = [
        "Luna", "Mika", "Boki", "Nina", "Rex", "Maya", "Toby", "Kira", "Coco", "Ziko",
        "Daisy", "Kiko", "Loki", "Nora", "Panda", "Milo", "Runa", "Tara", "Yoda", "Pip"
    ]

    active_animals = list(Animal.objects.filter(is_deleted=False).order_by("id"))
    seen_names = set()
    for animal in active_animals:
        if animal.name in seen_names:
            animal.is_deleted = True
            animal.save(update_fields=["is_deleted"])
        else:
            seen_names.add(animal.name)

    active_animals = list(Animal.objects.filter(is_deleted=False).order_by("id"))
    existing_names = {animal.name for animal in active_animals}

    for name in animal_names:
        if name not in existing_names:
            Animal.objects.create(name=name, status="Slobodna", is_deleted=False)
            existing_names.add(name)

    active_animals = list(Animal.objects.filter(is_deleted=False).order_by("id"))
    existing_requests = FosterRequest.objects.filter(is_deleted=False).count()
    if existing_requests < 10:
        for animal in active_animals[:10]:
            if FosterRequest.objects.filter(animal=animal, is_deleted=False).exists():
                continue
            FosterRequest.objects.create(animal=animal, status="Na čekanju", is_deleted=False)
            existing_requests += 1
            if existing_requests >= 10:
                break


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if username == "admin" and password == "admin123":
            request.session["is_admin_logged_in"] = True
            return redirect("animal_list")

        return render(request, "shelter/login.html", {"error": "Neispravno korisničko ime ili lozinka."})

    return render(request, "shelter/login.html")


def animal_list(request):
    ensure_seed_data()

    if not request.session.get("is_admin_logged_in"):
        return redirect("login")

    animals = Animal.objects.filter(is_deleted=False).order_by("name")
    adopted_animals = Animal.objects.filter(status="Udomljena").order_by("name")

    return render(
        request,
        "shelter/animal_list.html",
        {"animals": animals, "adopted_animals": adopted_animals},
    )


def request_list_view(request):
    ensure_seed_data()

    if not request.session.get("is_admin_logged_in"):
        return redirect("login")

    requests = FosterRequest.objects.filter(is_deleted=False).order_by("id")
    return render(request, "shelter/request_list.html", {"requests": requests})


def request_detail_view(request, request_id):
    ensure_seed_data()

    if not request.session.get("is_admin_logged_in"):
        return redirect("login")

    foster_request = get_object_or_404(FosterRequest, pk=request_id, is_deleted=False)
    animal = foster_request.animal

    if animal.status != "Udomljena":
        animal.status = "U Procesu"
        animal.save(update_fields=["status"])

    return render(request, "shelter/request_detail.html", {"request": foster_request, "animal": animal})


def close_request_view(request, request_id):
    ensure_seed_data()

    if not request.session.get("is_admin_logged_in"):
        return redirect("login")

    if request.method != "POST":
        return redirect("animal_list")

    foster_request = get_object_or_404(FosterRequest, pk=request_id, is_deleted=False)
    animal = foster_request.animal
    decision = request.POST.get("decision", "")

    if decision == "prihvacen":
        animal.status = "Udomljena"
        animal.is_deleted = True
        animal.save(update_fields=["status", "is_deleted"])

        foster_request.status = "Prihvaćen"
        foster_request.is_deleted = True
        foster_request.save(update_fields=["status", "is_deleted"])
        message = "Zahtjev prihvaćen"
    elif decision == "odbijen":
        animal.status = "Slobodna"
        animal.is_deleted = False
        animal.save(update_fields=["status", "is_deleted"])

        foster_request.status = "Odbijen"
        foster_request.is_deleted = True
        foster_request.save(update_fields=["status", "is_deleted"])
        message = "Zahtjev odbijen"
    else:
        message = "Odluka odložena"

    return render(request, "shelter/success.html", {"message": message})


def return_animal_view(request, animal_id):
    ensure_seed_data()

    if not request.session.get("is_admin_logged_in"):
        return redirect("login")

    if request.method != "POST":
        return redirect("animal_list")

    animal = get_object_or_404(Animal, pk=animal_id)
    animal.status = "Slobodna"
    animal.is_deleted = False
    animal.save(update_fields=["status", "is_deleted"])

    return render(request, "shelter/success.html", {"message": "Životinja vraćena"})
