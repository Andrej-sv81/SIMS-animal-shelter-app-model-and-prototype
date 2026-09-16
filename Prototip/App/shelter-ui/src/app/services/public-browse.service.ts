import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { Organization, OrganizationApiService } from './organization-api.service';
import { Animal, AnimalApiService } from './animal-api.service';

@Injectable({ providedIn: 'root' })
export class PublicBrowseService {
  private readonly organizations = inject(OrganizationApiService);
  private readonly animals = inject(AnimalApiService);

  getOrganizations(): Observable<Organization[]> {
    return this.organizations.getOrganizations();
  }
  getOrganization(id: number): Observable<Organization> {
    return this.organizations.getOrganization(id);
  }
  getOrganizationAnimals(id: number): Observable<Animal[]> {
    return this.animals.getAnimals(id);
  }
  getAllAnimals(): Observable<Animal[]> {
    return this.animals.getAllAnimals();
  }
}
