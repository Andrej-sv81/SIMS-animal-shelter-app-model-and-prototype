import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, map, tap } from 'rxjs';
import { Router, CanActivateFn } from '@angular/router';
import { OrganizationApiService } from './organization-api.service';

export interface LoginResponse {
  userId: number;
  firstName: string;
  lastName: string;
  email: string;
  role: string;
  organizationId: number | null;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly router = inject(Router);
  private readonly apiUrl = 'http://localhost:8080/api/auth';
  private readonly storageKey = 'shelter-auth-user';

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login`, { email, password }).pipe(
      tap((user) => localStorage.setItem(this.storageKey, JSON.stringify(user)))
    );
  }

  logout(): void {
    localStorage.removeItem(this.storageKey);
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.storageKey);
  }

  currentUser(): LoginResponse | null {
    const storedUser = localStorage.getItem(this.storageKey);
    return storedUser ? JSON.parse(storedUser) as LoginResponse : null;
  }

  isSuperAdmin(): boolean {
    return this.currentUser()?.role === 'SUPER_ADMIN';
  }

  isOrganizationScoped(): boolean {
    const role = this.currentUser()?.role;
    return role === 'ORGANIZATION_ADMIN' || role === 'VOLUNTEER';
  }
}

export const authGuard: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);
  return auth.isLoggedIn() ? true : router.createUrlTree(['/login']);
};

export const organizationAccessGuard: CanActivateFn = (route) => {
  const auth = inject(AuthService);
  const organizationApi = inject(OrganizationApiService);
  const router = inject(Router);
  const user = auth.currentUser();

  if (auth.isSuperAdmin() || !user) {
    return auth.isLoggedIn() ? true : router.createUrlTree(['/login']);
  }

  if (auth.isOrganizationScoped() && user.organizationId) {
    return String(user.organizationId) === route.paramMap.get('organizationId')
      ? true
      : router.createUrlTree(['/organizations']);
  }

  return organizationApi.getOrganizationForAdmin(user.userId).pipe(
    map((organization) => String(organization.id) === route.paramMap.get('organizationId')
      ? true
      : router.createUrlTree(['/organizations']))
  );
};
