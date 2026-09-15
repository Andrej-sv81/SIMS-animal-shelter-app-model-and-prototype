import { Component, OnInit, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { Organization, OrganizationApiService } from '../../services/organization-api.service';

@Component({ selector: 'app-public-organizations', imports: [RouterLink], templateUrl: './public-organizations.component.html', styleUrl: './public-organizations.component.css' })
export class PublicOrganizationsComponent implements OnInit {
  private readonly api = inject(OrganizationApiService);
  protected organizations: Organization[] = [];
  protected loading = true;
  protected error = '';
  ngOnInit(): void { this.api.getOrganizations().subscribe({ next: (items) => { this.organizations = items; this.loading = false; }, error: () => { this.error = 'Organizations could not be loaded.'; this.loading = false; } }); }
}
