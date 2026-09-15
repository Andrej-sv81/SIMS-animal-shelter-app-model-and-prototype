import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Admin {
  id: number;
  firstName: string;
  lastName: string;
  email: string;
  phone: string;
  active: boolean;
  joinedAt: string | null;
}

export interface Organization {
  id: number;
  name: string;
  description: string;
  bankAccount: string;
  admin: Admin;
}

export interface OrganizationRequest {
  name: string;
  description: string;
  bankAccount: string;
  adminFirstName: string;
  adminLastName: string;
  adminEmail: string;
  adminPhone: string;
  adminPassword: string;
}

@Injectable({ providedIn: 'root' })
export class OrganizationApiService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/api/organizations';

  getOrganizations(): Observable<Organization[]> {
    return this.http.get<Organization[]>(this.apiUrl);
  }

  getOrganization(id: number): Observable<Organization> {
    return this.http.get<Organization>(`${this.apiUrl}/${id}`);
  }

  getOrganizationForAdmin(adminId: number): Observable<Organization> {
    return this.http.get<Organization>(`${this.apiUrl}/mine/${adminId}`);
  }

  createOrganization(request: OrganizationRequest): Observable<Organization> {
    return this.http.post<Organization>(this.apiUrl, request);
  }

  updateOrganization(id: number, request: OrganizationRequest): Observable<Organization> {
    return this.http.put<Organization>(`${this.apiUrl}/${id}`, request);
  }

  deleteOrganization(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }
}
