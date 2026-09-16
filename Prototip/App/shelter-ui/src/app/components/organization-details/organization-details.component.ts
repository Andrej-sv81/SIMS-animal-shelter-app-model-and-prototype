import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Animal, AnimalApiService } from '../../services/animal-api.service';
import { AuthService } from '../../services/auth.service';
import {
  Organization,
  OrganizationApiService,
  OrganizationRequest,
} from '../../services/organization-api.service';

interface OrganizationEditForm extends OrganizationRequest {
  adminPasswordConfirm: string;
}

@Component({
  selector: 'app-organization-details',
  imports: [FormsModule, RouterLink],
  templateUrl: './organization-details.component.html',
  styleUrl: './organization-details.component.css',
})
export class OrganizationDetailsComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly organizationApi = inject(OrganizationApiService);
  private readonly animalApi = inject(AnimalApiService);
  private readonly auth = inject(AuthService);

  protected organization: Organization | null = null;
  protected animals: Animal[] = [];
  protected form: OrganizationEditForm = this.emptyForm();
  protected editing = false;
  protected loading = true;
  protected saving = false;
  protected error = '';
  protected notice = '';
  protected get canManageOrganization(): boolean {
    return this.auth.isSuperAdmin() || this.auth.currentUser()?.role === 'ORGANIZATION_ADMIN';
  }
  protected get canDeleteOrganization(): boolean {
    return this.auth.isSuperAdmin();
  }
  private organizationId = 0;

  ngOnInit(): void {
    this.organizationId = Number(this.route.snapshot.paramMap.get('organizationId'));
    if (!this.organizationId) {
      this.error = 'Invalid organization.';
      this.loading = false;
      return;
    }
    this.loadOrganization();
  }

  protected startEditing(): void {
    if (!this.organization) return;
    this.form = {
      name: this.organization.name,
      description: this.organization.description,
      bankAccount: this.organization.bankAccount,
      adminFirstName: this.organization.admin.firstName,
      adminLastName: this.organization.admin.lastName,
      adminEmail: this.organization.admin.email,
      adminPhone: this.organization.admin.phone,
      adminPassword: '',
      adminPasswordConfirm: '',
    };
    this.editing = true;
    this.clearMessages();
  }

  protected cancelEditing(): void {
    this.editing = false;
    this.clearMessages();
  }

  protected saveOrganization(): void {
    this.clearMessages();

    if (this.form.adminPassword && this.form.adminPassword !== this.form.adminPasswordConfirm) {
      this.error = 'Passwords do not match.';
      return;
    }

    if (this.form.adminPassword && !this.form.adminPasswordConfirm) {
      this.error = 'Please confirm the new password.';
      return;
    }

    this.saving = true;
    const { adminPasswordConfirm, ...request } = this.form;
    const payload: Partial<OrganizationRequest> & Record<string, unknown> = { ...request };

    if (!payload.adminPassword || !String(payload.adminPassword).trim()) {
      delete payload.adminPassword;
    }

    this.organizationApi
      .updateOrganization(this.organizationId, payload as OrganizationRequest)
      .subscribe({
        next: (organization) => {
          this.organization = organization;
          this.editing = false;
          this.saving = false;
          this.notice = 'Organization updated successfully.';
        },
        error: (response) => {
          this.error =
            response.error?.detail ||
            response.error?.message ||
            'The organization could not be updated.';
          this.saving = false;
        },
      });
  }

  protected removeOrganization(): void {
    if (!this.organization || !window.confirm(`Delete ${this.organization.name}?`)) return;
    this.organizationApi.deleteOrganization(this.organizationId).subscribe({
      next: () => this.router.navigate(['/organizations']),
      error: () => (this.error = 'The organization could not be deleted.'),
    });
  }

  protected animalImageUrl(animal: Animal): string {
    return animal?.imageUrl?.trim() || 'https://placehold.co/600x400/183b3b/fffdf8?text=No+image';
  }

  private loadOrganization(): void {
    this.organizationApi.getOrganization(this.organizationId).subscribe({
      next: (organization) => {
        this.organization = organization;
        this.loadAnimals();
      },
      error: () => {
        this.error = 'The organization could not be loaded.';
        this.loading = false;
      },
    });
  }

  private loadAnimals(): void {
    this.animalApi.getAnimals(this.organizationId).subscribe({
      next: (animals) => {
        this.animals = animals;
        this.loading = false;
      },
      error: () => {
        this.error = 'The animals could not be loaded.';
        this.loading = false;
      },
    });
  }

  private clearMessages(): void {
    this.error = '';
    this.notice = '';
  }

  private emptyForm(): OrganizationEditForm {
    return {
      name: '',
      description: '',
      bankAccount: '',
      adminFirstName: '',
      adminLastName: '',
      adminEmail: '',
      adminPhone: '',
      adminPassword: '',
      adminPasswordConfirm: '',
    };
  }
}
