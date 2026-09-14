import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import {
  Organization,
  OrganizationApiService,
  OrganizationRequest
} from '../../services/organization-api.service';

interface OrganizationForm extends OrganizationRequest {
  adminPasswordConfirm: string;
}

@Component({
  selector: 'app-organization-management',
  imports: [FormsModule, RouterLink],
  templateUrl: 'organization-management.component.html',
  styleUrl: 'organization-management.component.css'
})
export class OrganizationManagementComponent implements OnInit {
  private readonly organizationApi = inject(OrganizationApiService);
  protected organizations: Organization[] = [];
  protected form: OrganizationForm = this.emptyForm();
  protected editingId: number | null = null;
  protected newOrganizationOpen = false;
  protected loading = true;
  protected error = '';
  protected notice = '';
  protected saving = false;

  ngOnInit(): void {
    this.loadOrganizations();
  }

  protected saveOrganization(): void {
    this.clearMessages();
    if (this.editingId === null && this.form.adminPassword !== this.form.adminPasswordConfirm) {
      this.error = 'Administrator passwords do not match.';
      return;
    }

    this.saving = true;
    const { adminPasswordConfirm, ...request } = this.form;
    const operation = this.editingId === null
      ? this.organizationApi.createOrganization(request)
      : this.organizationApi.updateOrganization(this.editingId, request);

    operation.subscribe({
      next: () => {
        this.notice = this.editingId === null
          ? 'Organization created successfully.'
          : 'Organization updated successfully.';
        this.resetForm();
        this.loadOrganizations();
      },
      error: (response) => {
        const backendMessage = response.error?.detail || response.error?.message || '';
        const duplicateEmail = /email.*(already|exists)|already.*email|registered.*email/i.test(backendMessage)
          || response.status === 409;

        this.error = duplicateEmail
          ? 'This administrator email is already registered. Please use a different email address.'
          : backendMessage || 'The organization could not be saved.';
        this.saving = false;
      }
    });
  }

  protected editOrganization(organization: Organization): void {
    this.clearMessages();
    this.newOrganizationOpen = true;
    this.editingId = organization.id;
    this.form = {
      name: organization.name,
      description: organization.description,
      bankAccount: organization.bankAccount,
      adminFirstName: organization.admin.firstName,
      adminLastName: organization.admin.lastName,
      adminEmail: organization.admin.email,
      adminPhone: organization.admin.phone,
      adminPassword: '',
      adminPasswordConfirm: ''
    };
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  protected removeOrganization(organization: Organization): void {
    if (!window.confirm(`Delete ${organization.name}?`)) {
      return;
    }

    this.clearMessages();
    this.organizationApi.deleteOrganization(organization.id).subscribe({
      next: () => {
        this.notice = 'Organization deleted successfully.';
        this.loadOrganizations();
      },
      error: () => {
        this.error = 'The organization could not be deleted.';
      }
    });
  }

  protected cancelEdit(): void {
    this.resetForm();
    this.clearMessages();
  }

  protected toggleNewOrganization(): void {
    this.newOrganizationOpen = !this.newOrganizationOpen;
    if (!this.newOrganizationOpen) {
      this.resetForm();
      this.clearMessages();
    }
  }

  private loadOrganizations(): void {
    this.loading = true;
    this.organizationApi.getOrganizations().subscribe({
      next: (organizations) => {
        this.organizations = organizations;
        this.loading = false;
      },
      error: () => {
        this.error = 'The API is unavailable. Start the Spring Boot service on port 8080.';
        this.loading = false;
        this.saving = false;
      }
    });
  }

  private resetForm(): void {
    this.form = this.emptyForm();
    this.editingId = null;
    this.saving = false;
  }

  private clearMessages(): void {
    this.error = '';
    this.notice = '';
  }

  private emptyForm(): OrganizationForm {
    return {
      name: '',
      description: '',
      bankAccount: '',
      adminFirstName: '',
      adminLastName: '',
      adminEmail: '',
      adminPhone: '',
      adminPassword: '',
      adminPasswordConfirm: ''
    };
  }
}