import { Component, OnInit, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Animal } from '../../services/animal-api.service';
import { PublicBrowseService } from '../../services/public-browse.service';

@Component({ selector: 'app-public-animals', imports: [FormsModule, RouterLink], templateUrl: './public-animals.component.html', styleUrl: './public-animals.component.css' })
export class PublicAnimalsComponent implements OnInit {
  private readonly browse = inject(PublicBrowseService); protected animals: Animal[] = []; protected query = ''; protected loading = true; protected error = '';
  ngOnInit(): void { this.browse.getAllAnimals().subscribe({ next: (items) => { this.animals = items; this.loading = false; }, error: () => { this.error = 'Animals could not be loaded.'; this.loading = false; } }); }
  protected get filteredAnimals(): Animal[] { const q = this.query.trim().toLowerCase(); return !q ? this.animals : this.animals.filter(a => a.name.toLowerCase().includes(q) || a.species.toLowerCase().includes(q)); }
  protected image(animal: Animal): string { return animal.imageUrls?.[0] || animal.imageUrl || 'https://placehold.co/600x400/183b3b/fffdf8?text=No+image'; }
}
