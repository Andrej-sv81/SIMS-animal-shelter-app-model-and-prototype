from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Case, IntegerField, When
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AdoptionRequestForm,
    AdopterForm,
    AnimalForm,
    BankStatementForm,
    LoginForm,
    OrganizationCreateForm,
    OrganizationEditForm,
    VolunteerRegistrationForm,
)
from .models import (
    Adopter,
    Animal,
    BankStatement,
    BankStatementLine,
    FosterRequest,
    Organization,
    OrganizationMembership,
)
from .seed import initialize_seed_data


def home(request):
    initialize_seed_data()
    organizations = Organization.objects.filter(is_active=True).order_by("name")
    return render(request, "shelter/home.html", {"organizations": organizations})


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is not None:
            auth_login(request, user)
            return redirect("organization_list")
        messages.error(request, "Neispravno korisničko ime ili lozinka.")
    return render(request, "shelter/login.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    messages.success(request, "Odjava uspješna.")
    return redirect("home")


def register_volunteer(request):
    form = VolunteerRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password1"],
        )
        membership = OrganizationMembership.objects.create(
            user=user,
            organization=form.cleaned_data["organization"],
            role=OrganizationMembership.ROLE_VOLUNTEER,
        )
        auth_login(request, user)
        messages.success(request, "Registracija uspješna. Dobrodošli.")
        return redirect("organization_detail", organization_id=membership.organization.id)
    return render(request, "shelter/register_volunteer.html", {"form": form})


def create_organization(request):
    form = OrganizationCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        organization = form.save()
        user = User.objects.create_user(
            username=form.cleaned_data["admin_username"],
            email=form.cleaned_data["admin_email"],
            password=form.cleaned_data["admin_password"],
        )
        OrganizationMembership.objects.create(
            user=user,
            organization=organization,
            role=OrganizationMembership.ROLE_ADMIN,
        )
        messages.success(request, "Organizacija je stvorena i administrator je dodan.")
        return redirect("login")
    return render(request, "shelter/create_organization.html", {"form": form})


def _get_membership(user):
    if not user.is_authenticated:
        return None
    try:
        return user.membership
    except OrganizationMembership.DoesNotExist:
        return None


def _organization_required(view_func):
    def wrapper(request, *args, **kwargs):
        membership = _get_membership(request.user)
        if membership is None:
            messages.error(request, "Potrebna je registracija ili prijava.")
            return redirect("login")
        return view_func(request, membership=membership, *args, **kwargs)
    return wrapper


def _admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        membership = _get_membership(request.user)
        if membership is None or not membership.is_admin:
            messages.error(request, "Nedostaje ovlaštenje za tu akciju.")
            return redirect("organization_detail", organization_id=membership.organization.id if membership else 0)
        return view_func(request, membership=membership, *args, **kwargs)
    return wrapper


def organization_list(request):
    organizations = Organization.objects.filter(is_active=True).order_by("name")
    return render(request, "shelter/organization_list.html", {"organizations": organizations})


def animal_list(request):
    animals = Animal.objects.filter(is_deleted=False).select_related("organization").order_by("name")
    membership = _get_membership(request.user)
    return render(request, "shelter/animal_list.html", {"animals": animals, "membership": membership})


def organization_detail(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id, is_active=True)
    members = organization.members.all()
    animals = organization.animals.filter(is_deleted=False).order_by("name")
    volunteers = members.filter(role=OrganizationMembership.ROLE_VOLUNTEER)
    bank_statements = organization.bank_statements.all()
    membership = _get_membership(request.user)
    return render(
        request,
        "shelter/organization_detail.html",
        {
            "organization": organization,
            "animals": animals,
            "volunteers": volunteers,
            "bank_statements": bank_statements,
            "membership": membership,
        },
    )


@login_required(login_url="login")
def edit_organization(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id, is_active=True)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != organization or not membership.is_admin:
        messages.error(request, "Nedostaje ovlaštenje za uređivanje organizacije.")
        return redirect("organization_detail", organization_id=organization.id)
    form = OrganizationEditForm(request.POST or None, instance=organization)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Organizacija je ažurirana.")
        return redirect("organization_detail", organization_id=organization.id)
    return render(request, "shelter/edit_organization.html", {"form": form, "organization": organization})


@login_required(login_url="login")
def delete_organization(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id, is_active=True)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != organization or not membership.is_admin:
        messages.error(request, "Nedostaje ovlaštenje za brisanje organizacije.")
        return redirect("organization_detail", organization_id=organization.id)
    if request.method == "POST":
        organization.is_active = False
        organization.save(update_fields=["is_active"])
        messages.success(request, "Organizacija je uklonjena.")
        return redirect("organization_list")
    return render(request, "shelter/delete_organization.html", {"organization": organization})


def _owns_organization(user, organization):
    membership = _get_membership(user)
    return membership is not None and membership.organization == organization


def _can_manage_organization(user, organization):
    membership = _get_membership(user)
    return membership is not None and membership.organization == organization


@login_required(login_url="login")
def add_animal(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id, is_active=True)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != organization:
        messages.error(request, "Nedostaje ovlaštenje za dodavanje životinja.")
        return redirect("organization_detail", organization_id=organization.id)
    form = AnimalForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        animal = form.save(commit=False)
        animal.organization = organization
        animal.save()
        messages.success(request, "Životinja je dodana.")
        return redirect("organization_detail", organization_id=organization.id)
    return render(request, "shelter/add_animal.html", {"form": form, "organization": organization})


@login_required(login_url="login")
def edit_animal(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, is_deleted=False)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != animal.organization:
        messages.error(request, "Nedostaje ovlaštenje za uređivanje životinje.")
        return redirect("organization_detail", organization_id=animal.organization.id)
    form = AnimalForm(request.POST or None, request.FILES or None, instance=animal)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Životinja je ažurirana.")
        return redirect("animal_detail", animal_id=animal.id)
    return render(request, "shelter/edit_animal.html", {"form": form, "animal": animal})


@login_required(login_url="login")
def delete_animal(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, is_deleted=False)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != animal.organization:
        messages.error(request, "Nedostaje ovlaštenje za brisanje životinje.")
        return redirect("organization_detail", organization_id=animal.organization.id)
    if request.method == "POST":
        animal.is_deleted = True
        animal.save(update_fields=["is_deleted"])
        messages.success(request, "Životinja je uklonjena.")
        return redirect("organization_detail", organization_id=animal.organization.id)
    return render(request, "shelter/delete_animal.html", {"animal": animal})


def animal_detail(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, is_deleted=False)
    request_form = AdoptionRequestForm()
    membership = _get_membership(request.user)
    is_member = membership is not None and membership.organization == animal.organization
    animal_requests = animal.requests.filter(is_deleted=False).order_by("-created_at")
    return render(
        request,
        "shelter/animal_detail.html",
        {
            "animal": animal,
            "request_form": request_form,
            "is_member": is_member,
            "membership": membership,
            "animal_requests": animal_requests,
        },
    )


@login_required(login_url="login")
def foster_animal(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, is_deleted=False)
    membership = _get_membership(request.user)
    if membership is None or not membership.is_volunteer or membership.organization != animal.organization:
        messages.error(request, "Nedostaje ovlaštenje za privremeno skrbništvo.")
        return redirect("animal_detail", animal_id=animal.id)
    animal.fostered_by = request.user
    animal.fostered_at = timezone.now()
    animal.status = Animal.STATUS_PROCESS
    animal.save(update_fields=["fostered_by", "fostered_at", "status"])
    messages.success(request, "Životinja je uzeta u privremeno skrbništvo.")
    return redirect("animal_detail", animal_id=animal.id)


def submit_adoption_request(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id, is_deleted=False)
    if request.method == "POST":
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            foster_request = FosterRequest.objects.create(
                animal=animal,
                applicant_first_name=form.cleaned_data["first_name"],
                applicant_last_name=form.cleaned_data["last_name"],
                applicant_phone=form.cleaned_data["phone"],
                applicant_email=form.cleaned_data["email"],
                message=form.cleaned_data["message"],
                status=FosterRequest.STATUS_CHOICES[0][0],
            )
            if animal.status == Animal.STATUS_FREE:
                animal.status = Animal.STATUS_PROCESS
                animal.save(update_fields=["status"])
            messages.success(request, "Zahtjev za udomljavanje je poslan.")
            return redirect("animal_detail", animal_id=animal.id)
    else:
        form = AdoptionRequestForm()
    return render(request, "shelter/submit_adoption_request.html", {"animal": animal, "form": form})


def request_list(request):
    membership = _get_membership(request.user)
    if membership is None:
        return redirect("login")
    requests = FosterRequest.objects.filter(
        animal__organization=membership.organization,
        is_deleted=False,
    ).order_by(
        Case(
            When(status=FosterRequest.STATUS_CHOICES[0][0], then=0),
            default=1,
            output_field=IntegerField(),
        ),
        "-created_at",
    )
    return render(request, "shelter/request_list.html", {"requests": requests, "organization": membership.organization})


def request_detail(request, request_id):
    foster_request = get_object_or_404(FosterRequest, pk=request_id, is_deleted=False)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != foster_request.animal.organization:
        messages.error(request, "Nedostaje ovlaštenje za pregled zahtjeva.")
        return redirect("organization_list")
    return render(
        request,
        "shelter/request_detail.html",
        {"request": foster_request, "animal": foster_request.animal, "membership": membership},
    )


def close_request(request, request_id):
    foster_request = get_object_or_404(FosterRequest, pk=request_id, is_deleted=False)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != foster_request.animal.organization:
        messages.error(request, "Nedostaje ovlaštenje za zatvaranje zahtjeva.")
        return redirect("organization_list")
    if request.method != "POST":
        return redirect("request_detail", request_id=request_id)
    decision = request.POST.get("decision")
    if decision == "prihvacen":
        adopter, created = Adopter.objects.get_or_create(
            email=foster_request.applicant_email,
            organization=membership.organization,
            defaults={
                "first_name": foster_request.applicant_first_name,
                "last_name": foster_request.applicant_last_name,
                "phone": foster_request.applicant_phone,
                "created_by": request.user,
            },
        )
        foster_request.adopter = adopter
        foster_request.status = "Prihvaćen"
        foster_request.save(update_fields=["adopter", "status"])
        animal = foster_request.animal
        animal.status = Animal.STATUS_ADOPTED
        animal.adopter = adopter
        animal.save(update_fields=["status", "adopter"])
        messages.success(request, "Zahtjev je prihvaćen i životinja je udomljena.")
    elif decision == "odbijen":
        foster_request.status = "Odbijen"
        foster_request.save(update_fields=["status"])
        open_requests = FosterRequest.objects.filter(
            animal=foster_request.animal,
            status=FosterRequest.STATUS_CHOICES[0][0],
            is_deleted=False,
        ).exists()
        if not open_requests and foster_request.animal.status != Animal.STATUS_ADOPTED:
            foster_request.animal.status = Animal.STATUS_FREE
            foster_request.animal.save(update_fields=["status"])
        messages.success(request, "Zahtjev je odbijen.")
    else:
        messages.info(request, "Zahtjev je ostavljen otvorenim.")
    return redirect("request_detail", request_id=request_id)


@login_required(login_url="login")
def adopter_list(request):
    membership = _get_membership(request.user)
    if membership is None:
        return redirect("login")
    adopters = Adopter.objects.filter(organization=membership.organization, is_deleted=False)
    return render(request, "shelter/adopter_list.html", {"adopters": adopters})


@login_required(login_url="login")
def add_adopter(request):
    membership = _get_membership(request.user)
    if membership is None:
        return redirect("login")
    form = AdopterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        adopter = form.save(commit=False)
        adopter.organization = membership.organization
        adopter.created_by = request.user
        adopter.save()
        messages.success(request, "Udomitelj je dodan.")
        return redirect("adopter_list")
    return render(request, "shelter/add_adopter.html", {"form": form})


@login_required(login_url="login")
def organization_volunteers(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id, is_active=True)
    membership = _get_membership(request.user)
    if membership is None or membership.organization != organization or not membership.is_admin:
        messages.error(request, "Nedostaje ovlaštenje za pregled volontera.")
        return redirect("organization_detail", organization_id=organization.id)
    volunteers = organization.members.filter(role=OrganizationMembership.ROLE_VOLUNTEER)
    return render(request, "shelter/organization_volunteers.html", {"organization": organization, "volunteers": volunteers})


@login_required(login_url="login")
def bank_statement_list(request):
    membership = _get_membership(request.user)
    if membership is None:
        return redirect("login")
    statements = BankStatement.objects.filter(organization=membership.organization)
    return render(request, "shelter/bank_statement_list.html", {"statements": statements})


@login_required(login_url="login")
def upload_bank_statement(request):
    membership = _get_membership(request.user)
    if membership is None or not membership.is_admin:
        messages.error(request, "Nedostaje ovlaštenje za uvoz bankovnih izvoda.")
        return redirect("organization_detail", organization_id=membership.organization.id if membership else 0)
    form = BankStatementForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        statement = form.save(commit=False)
        statement.organization = membership.organization
        statement.uploaded_by = request.user
        statement.save()
        file = statement.file
        if file.name.lower().endswith(".csv"):
            try:
                import csv
                import io

                file.open()
                reader = csv.DictReader(io.TextIOWrapper(file, encoding="utf-8"))
                for row in reader:
                    if not row.get("date") or not row.get("amount"):
                        continue
                    BankStatementLine.objects.create(
                        statement=statement,
                        date=row.get("date"),
                        description=row.get("description", ""),
                        amount=row.get("amount"),
                        balance=row.get("balance", 0),
                    )
            except Exception:
                pass
        messages.success(request, "Bankovni izvještaj je uspješno učitan.")
        return redirect("bank_statement_list")
    return render(request, "shelter/upload_bank_statement.html", {"form": form})


@user_passes_test(lambda user: user.is_superuser, login_url="login")
def system_users(request):
    users = User.objects.order_by("username")
    return render(request, "shelter/system_users.html", {"users": users})


def initialize_data(request):
    initialize_seed_data()
    messages.success(request, "Početni podaci su dodani.")
    return redirect("home")
