import { Component, Input } from '@angular/core';

import { Organization } from '../organization.model';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'volontulo-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.scss'],
})

export class OrganizationDetailsComponent {
  @Input() isUserOrgMember: boolean;
  @Input() organization: Organization;
  djangoRoot: string = environment.djangoRoot;
}
