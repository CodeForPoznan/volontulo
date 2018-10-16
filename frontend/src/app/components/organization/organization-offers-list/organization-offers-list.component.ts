import { Component, Input } from '@angular/core';

import { Offer } from 'app/models/offer.model';
import { environment } from 'environments/environment';

@Component({
  selector: 'volontulo-organization-offers-list',
  templateUrl: './organization-offers-list.component.html',
  styleUrls: ['./organization-offers-list.component.scss'],
})

export class OrganizationOffersListComponent {
  @Input() isUserOrgMember: boolean;
  @Input() offers: Offer[];
  djangoRoot: string = environment.djangoRoot;
}
