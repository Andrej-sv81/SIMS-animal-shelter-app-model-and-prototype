import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { Animal, AnimalApiService, AnimalRequest } from '../../services/animal-api.service';

@Component({
  selector: 'app-animal-details',
  imports: [FormsModule, RouterLink],
  templateUrl: './animal-details.component.html',
  styleUrl: './animal-details.component.css'
})
export class AnimalDetailsComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly animalApi = inject(AnimalApiService);

  protected animal: Animal | null = null;
  protected form: AnimalRequest = this.emptyForm();
  protected organizationId = 0;
  protected animalId = 0;
  protected editing = false;
  protected loading = true;
  protected saving = false;
  protected error = '';
  protected notice = '';
  protected selectedFiles: File[] = [];

  ngOnInit(): void {
    this.organizationId = Number(this.route.snapshot.paramMap.get('organizationId'));
    this.animalId = Number(this.route.snapshot.paramMap.get('animalId'));
    if (!this.organizationId || !this.animalId) {
      this.error = 'Invalid animal.';
      this.loading = false;
      return;
    }
    this.loadAnimal();
  }

  protected startEditing(): void {
    if (!this.animal) return;
    this.form = this.toRequest(this.animal);
    this.selectedFiles = [];
    this.editing = true;
    this.clearMessages();
  }

  protected cancelEditing(): void {
    this.editing = false;
    this.selectedFiles = [];
    this.clearMessages();
  }

  protected onImageSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFiles = Array.from(input.files ?? []);
    if (this.selectedFiles[0]) {
      this.form.imageUrl = URL.createObjectURL(this.selectedFiles[0]);
    }
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
    this.animalApi.updateAnimal(this.organizationId, this.animalId, this.form, this.selectedFiles).subscribe({
      next: (animal) => {
        this.animal = animal;
        this.form = this.toRequest(animal);
        this.editing = false;
        this.selectedFiles = [];
        this.saving = false;
        this.notice = 'Animal updated successfully.';
      },
      error: () => {
        this.error = 'The animal could not be updated.';
        this.saving = false;
      }
    });
  }

  protected removeAnimal(): void {
    if (!this.animal || !window.confirm(`Delete ${this.animal.name}?`)) return;
    this.animalApi.deleteAnimal(this.organizationId, this.animalId).subscribe({
      next: () => this.router.navigate(['/organizations', this.organizationId]),
      error: () => this.error = 'The animal could not be deleted.'
    });
  }

  protected removeImage(imageUrl: string): void {
    if (!this.animal || !window.confirm('Remove this image?')) return;
    this.animalApi.deleteAnimalImage(this.organizationId, this.animalId, imageUrl).subscribe({
      next: () => {
        if (!this.animal) return;
        const imageUrls = this.imageUrls().filter((url) => url !== imageUrl);
        this.animal = { ...this.animal, imageUrl: imageUrls[0] || '', imageUrls };
        this.form = this.toRequest(this.animal);
        this.notice = 'Image removed successfully.';
      },
      error: () => this.error = 'The image could not be removed.'
    });
  }

  protected imageUrl(): string {
    return this.imageUrls()[0] || 'https://placehold.co/900x600/183b3b/fffdf8?text=No+image';
  }

  protected imageUrls(): string[] {
    if (!this.animal) return [];
    return this.animal.imageUrls?.length ? this.animal.imageUrls : (this.animal.imageUrl ? [this.animal.imageUrl] : []);
  }

  protected statusLabel(status: string): string {
    return { FREE: 'Free', ADOPTED: 'Adopted', IN_PROCESS: 'In process' }[status] || status;
  }

  protected genderLabel(gender: string): string {
    return gender === 'FEMALE' ? 'Female' : 'Male';
  }

  private loadAnimal(): void {
    this.animalApi.getAnimal(this.organizationId, this.animalId).subscribe({
      next: (animal) => {
        this.animal = animal;
        this.form = this.toRequest(animal);
        this.loading = false;
      },
      error: () => {
        this.error = 'The animal could not be loaded.';
        this.loading = false;
      }
    });
  }

  private toRequest(animal: Animal): AnimalRequest {
    return {
      name: animal.name,
      species: animal.species,
      age: animal.age,
      gender: animal.gender,
      healthDescription: animal.healthDescription || '',
      behaviorNotes: animal.behaviorNotes || '',
      status: animal.status,
      imageUrl: animal.imageUrl || '',
      adopter: animal.adopter || ''
    };
  }

  private emptyForm(): AnimalRequest {
    return {
      name: '', species: '', age: 0, gender: 'MALE', healthDescription: '',
      behaviorNotes: '', status: 'FREE', imageUrl: '', adopter: ''
    };
  }

  private clearMessages(): void {
    this.error = '';
    this.notice = '';
  }
}
