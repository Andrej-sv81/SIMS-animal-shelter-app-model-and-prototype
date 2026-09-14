import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import {
  Animal,
  AnimalApiService,
  AnimalRequest
} from '../../services/animal-api.service';
import { Organization, OrganizationApiService } from '../../services/organization-api.service';

@Component({
  selector: 'app-animal-management',
  imports: [FormsModule, RouterLink],
  templateUrl: './animal-management.component.html',
  styleUrl: './animal-management.component.css'
})
export class AnimalManagementComponent implements OnInit {
  protected organizationId = 0;
  protected organization: Organization | null = null;
  private readonly route = inject(ActivatedRoute);
  private readonly animalApi = inject(AnimalApiService);
  private readonly organizationApi = inject(OrganizationApiService);
  protected animals: Animal[] = [];
  protected form: AnimalRequest = this.emptyForm();
  protected editingId: number | null = null;
  protected selectedFiles: File[] = [];
  protected loading = true;
  protected saving = false;
  protected error = '';
  protected notice = '';

  ngOnInit(): void {
    const organizationId = Number(this.route.snapshot.paramMap.get('organizationId'));
    if (!organizationId) {
      this.error = 'Invalid organization.';
      this.loading = false;
      return;
    }

    this.organizationId = organizationId;
    this.organizationApi.getOrganization(organizationId).subscribe({
      next: (organization) => {
        this.organization = organization;
        this.loadAnimals();
      },
      error: () => {
        this.error = 'The organization could not be loaded.';
        this.loading = false;
      }
    });
  }

  protected onImageSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFiles = Array.from(input.files ?? []);
    this.form.imageUrl = this.selectedFiles[0] ? URL.createObjectURL(this.selectedFiles[0]) : this.form.imageUrl;
  }

  protected onStatusChange(status: string): void {
    this.form.status = status;
    if (status === 'FREE') {
      this.form.adopter = '';
    }
  }

  protected saveAnimal(): void {
    this.clearMessages();
    this.saving = true;
    const request: AnimalRequest = {
      name: this.form.name,
      species: this.form.species,
      age: this.form.age,
      gender: this.form.gender,
      healthDescription: this.form.healthDescription,
      behaviorNotes: this.form.behaviorNotes,
      status: this.form.status,
      adopter: this.form.adopter,
      imageUrl: this.selectedFiles[0] ? URL.createObjectURL(this.selectedFiles[0]) : this.form.imageUrl
    };

    const operation = this.editingId === null
      ? this.animalApi.createAnimal(this.organizationId, request, this.selectedFiles)
      : this.animalApi.updateAnimal(this.organizationId, this.editingId, request, this.selectedFiles);

    operation.subscribe({
      next: () => {
        this.notice = this.editingId === null
          ? 'Animal created successfully.'
          : 'Animal updated successfully.';
        this.resetForm();
        this.loadAnimals();
      },
      error: () => {
        this.error = 'The animal could not be saved.';
        this.saving = false;
      }
    });
  }

  protected editAnimal(animal: Animal): void {
    this.clearMessages();
    this.editingId = animal.id;
    this.form = {
      name: animal.name,
      species: animal.species,
      age: animal.age,
      gender: animal.gender,
      healthDescription: animal.healthDescription,
      behaviorNotes: animal.behaviorNotes,
      adopter: animal.adopter,
      status: animal.status,
      imageUrl: animal.imageUrl
    };
  }

  protected removeAnimal(animal: Animal): void {
    if (!window.confirm(`Delete ${animal.name}?`)) {
      return;
    }

    this.clearMessages();
    this.animalApi.deleteAnimal(this.organizationId, animal.id).subscribe({
      next: () => {
        this.notice = 'Animal deleted successfully.';
        this.loadAnimals();
      },
      error: () => {
        this.error = 'The animal could not be deleted.';
      }
    });
  }

  protected cancelEdit(): void {
    this.resetForm();
    this.clearMessages();
  }

  private loadAnimals(): void {
    this.loading = true;
    this.animalApi.getAnimals(this.organizationId).subscribe({
      next: (animals) => {
        this.animals = animals;
        this.loading = false;
      },
      error: () => {
        this.error = 'Animals could not be loaded.';
        this.loading = false;
      }
    });
  }

  private resetForm(): void {
    this.form = this.emptyForm();
    this.selectedFiles = [];
    this.editingId = null;
    this.saving = false;
  }

  private clearMessages(): void {
    this.error = '';
    this.notice = '';
  }

  private emptyForm(): AnimalRequest {
    return {
      name: '',
      species: '',
      age: 0,
      gender: 'MALE',
      healthDescription: '',
      behaviorNotes: '',
      status: 'FREE',
      imageUrl: '',
      adopter: ''
    };
  }
}