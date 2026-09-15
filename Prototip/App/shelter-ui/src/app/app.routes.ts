import { Routes } from '@angular/router';
import { OrganizationManagementComponent } from './components/organization-management/organization-management.component';
import { AnimalManagementComponent } from './components/animal-management/animal-management.component';
import { AnimalDetailsComponent } from './components/animal-details/animal-details.component';
import { OrganizationDetailsComponent } from './components/organization-details/organization-details.component';
import { VolunteerManagementComponent } from './components/volunteer-management/volunteer-management.component';
import { LoginComponent } from './components/login/login.component';
import { authGuard, organizationAccessGuard } from './services/auth.service';
import { PublicOrganizationsComponent } from './components/public-organizations/public-organizations.component';
import { PublicOrganizationAnimalsComponent } from './components/public-organization-animals/public-organization-animals.component';
import { PublicAnimalsComponent } from './components/public-animals/public-animals.component';
import { PublicAnimalDetailsComponent } from './components/public-animal-details/public-animal-details.component';

export const routes: Routes = [
	{
		path: '',
		pathMatch: 'full',
		redirectTo: 'browse/organizations'
	},
	{
		path: 'login',
		component: LoginComponent
	},
	{
		path: 'browse/organizations',
		component: PublicOrganizationsComponent
	},
	{
		path: 'browse/organizations/:organizationId',
		component: PublicOrganizationAnimalsComponent
	},
	{
		path: 'browse/animals',
		component: PublicAnimalsComponent
	},
	{
		path: 'browse/animals/:animalId',
		component: PublicAnimalDetailsComponent
	},
	{
		path: 'organizations',
		component: OrganizationManagementComponent,
		canActivate: [authGuard]
	},
	{
		path: 'organizations/:organizationId',
		component: OrganizationDetailsComponent,
		canActivate: [authGuard, organizationAccessGuard]
	},
	{
		path: 'organizations/:organizationId/animals/:animalId',
		component: AnimalDetailsComponent,
		canActivate: [authGuard, organizationAccessGuard]
	},
	{
		path: 'organizations/:organizationId/animals',
		component: AnimalManagementComponent,
		canActivate: [authGuard, organizationAccessGuard]
	},
	{
		path: 'organizations/:organizationId/volunteers',
		component: VolunteerManagementComponent,
		canActivate: [authGuard, organizationAccessGuard]
	},
	{
		path: '**',
		redirectTo: 'organizations'
	}
];
