import { Component, Input } from '@angular/core';

import { Organization } from 'app/models/organization.model';

@Component({
  selector: 'volontulo-organizations-list',
  templateUrl: './organizations-list.component.html'
})
export class OrganizationsListComponent {
  @Input() organizations: Organization[];
}
