import { Routes } from '@angular/router';
import { OrganizationManagementComponent } from './components/organization-management/organization-management.component';
import { AnimalManagementComponent } from './components/animal-management/animal-management.component';
import { AnimalDetailsComponent } from './components/animal-details/animal-details.component';
import { OrganizationDetailsComponent } from './components/organization-details/organization-details.component';

export const routes: Routes = [
	{
		path: '',
		pathMatch: 'full',
		redirectTo: 'organizations'
	},
	{
		path: 'organizations',
		component: OrganizationManagementComponent
	},
	{
		path: 'organizations/:organizationId',
		component: OrganizationDetailsComponent
	},
	{
		path: 'organizations/:organizationId/animals/:animalId',
		component: AnimalDetailsComponent
	},
	{
		path: 'organizations/:organizationId/animals',
		component: AnimalManagementComponent
	},
	{
		path: '**',
		redirectTo: 'organizations'
	}
];
