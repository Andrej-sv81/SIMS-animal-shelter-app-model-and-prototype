import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Animal {
  id: number;
  name: string;
  species: string;
  age: number;
  gender: string;
  healthDescription: string;
  behaviorNotes: string;
  status: string;
  imageUrl: string;
  imageUrls: string[];
  adopter: string;
  organizationId: number;
  organizationName: string;
}

export interface AnimalRequest {
  name: string;
  species: string;
  age: number;
  gender: string;
  healthDescription: string;
  behaviorNotes: string;
  status: string;
  imageUrl: string;
  adopter: string;
}

@Injectable({ providedIn: 'root' })
export class AnimalApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8080/api/organizations';

  getAnimals(organizationId: number): Observable<Animal[]> {
    return this.http.get<Animal[]>(`${this.apiUrl}/${organizationId}/animals`);
  }

  getAllAnimals(): Observable<Animal[]> {
    return this.http.get<Animal[]>('http://localhost:8080/api/animals');
  }

  createAnimal(
    organizationId: number,
    request: AnimalRequest,
    imageFiles: File[] = [],
  ): Observable<Animal> {
    const formData = new FormData();
    formData.append('name', request.name);
    formData.append('species', request.species);
    formData.append('age', String(request.age));
    formData.append('gender', request.gender);
    formData.append('healthDescription', request.healthDescription);
    formData.append('behaviorNotes', request.behaviorNotes);
    formData.append('status', request.status);
    formData.append('adopter', request.adopter);
    for (const imageFile of imageFiles) {
      formData.append('image', imageFile);
    }
    return this.http.post<Animal>(`${this.apiUrl}/${organizationId}/animals`, formData);
  }

  updateAnimal(
    organizationId: number,
    animalId: number,
    request: AnimalRequest,
    imageFiles: File[] = [],
  ): Observable<Animal> {
    const formData = new FormData();
    formData.append('name', request.name);
    formData.append('species', request.species);
    formData.append('age', String(request.age));
    formData.append('gender', request.gender);
    formData.append('healthDescription', request.healthDescription);
    formData.append('behaviorNotes', request.behaviorNotes);
    formData.append('status', request.status);
    formData.append('adopter', request.adopter);
    for (const imageFile of imageFiles) {
      formData.append('image', imageFile);
    }
    return this.http.put<Animal>(`${this.apiUrl}/${organizationId}/animals/${animalId}`, formData);
  }

  getAnimal(organizationId: number, animalId: number): Observable<Animal> {
    return this.http.get<Animal>(`${this.apiUrl}/${organizationId}/animals/${animalId}`);
  }

  deleteAnimal(organizationId: number, animalId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${organizationId}/animals/${animalId}`);
  }

  deleteAnimalImage(organizationId: number, animalId: number, imageUrl: string): Observable<void> {
    const params = new HttpParams().set('imageUrl', imageUrl);
    return this.http.delete<void>(`${this.apiUrl}/${organizationId}/animals/${animalId}/images`, {
      params,
    });
  }
}
