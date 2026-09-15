import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Volunteer, VolunteerApiService, VolunteerRequest } from '../../services/volunteer-api.service';
import { Organization, OrganizationApiService } from '../../services/organization-api.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-volunteer-management',
  imports: [FormsModule, RouterLink],
  templateUrl: './volunteer-management.component.html',
  styleUrl: './volunteer-management.component.css'
})
export class VolunteerManagementComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly volunteerApi = inject(VolunteerApiService);
  private readonly organizationApi = inject(OrganizationApiService);
  private readonly auth = inject(AuthService);

  protected organizationId = 0;
  protected organization: Organization | null = null;
  protected volunteers: Volunteer[] = [];
  protected form: VolunteerRequest = this.emptyForm();
  protected loading = true;
  protected saving = false;
  protected error = '';
  protected notice = '';

  protected get canManageVolunteers(): boolean {
    const role = this.auth.currentUser()?.role;
    return role === 'SUPER_ADMIN' || role === 'ORGANIZATION_ADMIN';
  }

  ngOnInit(): void {
    this.organizationId = Number(this.route.snapshot.paramMap.get('organizationId'));
    if (!this.organizationId) {
      this.error = 'Invalid organization.';
      this.loading = false;
      return;
    }
    this.organizationApi.getOrganization(this.organizationId).subscribe({
      next: (organization) => {
        this.organization = organization;
        this.loadVolunteers();
      },
      error: () => {
        this.error = 'The organization could not be loaded.';
        this.loading = false;
      }
    });
  }

  protected saveVolunteer(): void {
    this.error = '';
    this.notice = '';
    if (this.form.password !== this.form.passwordConfirm) {
      this.error = 'Passwords do not match.';
      return;
    }
    this.saving = true;
    this.volunteerApi.createVolunteer(this.organizationId, this.form).subscribe({
      next: () => {
        this.notice = 'Volunteer registered successfully.';
        this.form = this.emptyForm();
        this.saving = false;
        this.loadVolunteers();
      },
      error: (response) => {
        this.error = response.error?.detail || response.error?.message || 'The volunteer could not be registered.';
        this.saving = false;
      }
    });
  }

  protected toggleActive(volunteer: Volunteer): void {
    this.volunteerApi.toggleActive(this.organizationId, volunteer.id).subscribe({
      next: (updatedVolunteer) => {
        volunteer.active = updatedVolunteer.active;
        this.notice = updatedVolunteer.active ? 'Volunteer activated.' : 'Volunteer deactivated.';
      },
      error: () => this.error = 'The volunteer status could not be changed.'
    });
  }

  private loadVolunteers(): void {
    this.volunteerApi.getVolunteers(this.organizationId).subscribe({
      next: (volunteers) => {
        this.volunteers = volunteers;
        this.loading = false;
      },
      error: () => {
        this.error = 'The volunteers could not be loaded.';
        this.loading = false;
      }
    });
  }

  private emptyForm(): VolunteerRequest {
    return { firstName: '', lastName: '', email: '', phone: '', password: '', passwordConfirm: '' };
  }
}
