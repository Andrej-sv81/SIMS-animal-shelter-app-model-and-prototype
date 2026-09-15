import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Organization, OrganizationApiService } from '../../services/organization-api.service';
import { Animal, AnimalApiService } from '../../services/animal-api.service';

@Component({ selector: 'app-public-organization-animals', imports: [RouterLink], templateUrl: './public-organization-animals.component.html', styleUrl: './public-organization-animals.component.css' })
export class PublicOrganizationAnimalsComponent implements OnInit {
  private readonly route = inject(ActivatedRoute); private readonly organizations = inject(OrganizationApiService); private readonly animalsApi = inject(AnimalApiService);
  protected organization: Organization | null = null; protected animals: Animal[] = []; protected loading = true; protected error = '';
  ngOnInit(): void { const id = Number(this.route.snapshot.paramMap.get('organizationId')); this.organizations.getOrganization(id).subscribe({ next: (org) => { this.organization = org; this.animalsApi.getAnimals(id).subscribe({ next: (items) => { this.animals = items; this.loading = false; }, error: () => { this.error = 'Animals could not be loaded.'; this.loading = false; } }); }, error: () => { this.error = 'Organization could not be loaded.'; this.loading = false; } }); }
  protected image(animal: Animal): string { return animal.imageUrls?.[0] || animal.imageUrl || 'https://placehold.co/600x400/183b3b/fffdf8?text=No+image'; }
}
