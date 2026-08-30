import { Component, OnInit, inject } from '@angular/core';
import { Animal, AnimalApiService } from './animal-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements OnInit {
  private readonly animalApi = inject(AnimalApiService);
  protected animals: Animal[] = [];
  protected loading = true;
  protected error = '';

  ngOnInit(): void {
    this.animalApi.getAnimals().subscribe({
      next: (animals) => {
        this.animals = animals;
        this.loading = false;
      },
      error: () => {
        this.error = 'The API is unavailable. Start the Spring Boot service on port 8080.';
        this.loading = false;
      }
    });
  }
}
