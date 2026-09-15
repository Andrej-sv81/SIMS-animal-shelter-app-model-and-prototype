import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Volunteer {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  active: boolean;
  joinedAt: string;
  organizationId: number;
}

export interface VolunteerRequest {
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  password: string;
  passwordConfirm: string;
}

@Injectable({ providedIn: 'root' })
export class VolunteerApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8080/api/organizations';

  getVolunteers(organizationId: number): Observable<Volunteer[]> {
    return this.http.get<Volunteer[]>(`${this.apiUrl}/${organizationId}/volunteers`);
  }

  createVolunteer(organizationId: number, request: VolunteerRequest): Observable<Volunteer> {
    const { passwordConfirm, ...payload } = request;
    return this.http.post<Volunteer>(`${this.apiUrl}/${organizationId}/volunteers`, payload);
  }

  toggleActive(organizationId: number, volunteerId: number): Observable<Volunteer> {
    return this.http.patch<Volunteer>(
      `${this.apiUrl}/${organizationId}/volunteers/${volunteerId}/active`,
      {},
    );
  }
}
