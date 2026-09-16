import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { Animal } from '../../services/animal-api.service';
import { PublicBrowseService } from '../../services/public-browse.service';

@Component({
  selector: 'app-public-animal-details',
  imports: [FormsModule, RouterLink],
  templateUrl: './public-animal-details.component.html',
  styleUrl: './public-animal-details.component.css',
})
export class PublicAnimalDetailsComponent implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly browse = inject(PublicBrowseService);

  protected animal: Animal | null = null;
  protected adoptionOpen = false;
  protected donationOpen = false;
  protected loading = true;
  protected error = '';
  protected adopter = { firstName: '', lastName: '', phone: '', email: '' };
  protected donation = { amount: 0, type: 'MONEY' };
  protected imageUrls(): string[] {
    if (!this.animal) return [];
    return this.animal.imageUrls?.length
      ? this.animal.imageUrls
      : this.animal.imageUrl
        ? [this.animal.imageUrl]
        : [];
  }
  protected image(image: string): string {
    return image || 'https://placehold.co/900x600/183b3b/fffdf8?text=No+image';
  }
  protected submitAdoption(): void {
    this.adoptionOpen = false;
  }
  protected submitDonation(): void {
    this.donationOpen = false;
  }

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('animalId'));
    this.browse.getAllAnimals().subscribe({
      next: (items) => {
        this.animal = items.find((item) => item.id === id) || null;
        this.loading = false;
      },
      error: () => {
        this.error = 'Animal could not be loaded.';
        this.loading = false;
      },
    });
  }
}
