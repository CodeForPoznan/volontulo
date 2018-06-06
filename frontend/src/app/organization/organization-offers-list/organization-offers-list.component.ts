import { Component, Input } from '@angular/core';

import { Offer } from '../../homepage-offer/offers.model';
import { environment } from '../../../environments/environment';
import { User } from '../../user';

@Component({
  selector: 'volontulo-organization-offers-list',
  templateUrl: './organization-offers-list.component.html',
  styleUrls: ['./organization-offers-list.component.scss'],
})

export class OrganizationOffersListComponent {
  @Input() isUserOrgMember: boolean;
  @Input() offers: Offer[];
  @Input() user: User;
  djangoRoot: string = environment.djangoRoot;
}
