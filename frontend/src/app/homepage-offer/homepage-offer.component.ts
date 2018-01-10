import { Component, OnInit, Input } from '@angular/core';

import { Offer } from './offers.model';
import { OffersService } from './offers.service';
import { OrganizationService } from '../organization/organization.service';
import { Organization } from '../organization/organization.model';

@Component({
  selector: 'volontulo-homepage-offer',
  templateUrl: './homepage-offer.component.html',
  styleUrls: ['./homepage-offer.component.css'],
  providers: [OffersService, OrganizationService]
})
export class HomepageOfferComponent {
  @Input() offer: Offer;

  constructor(private offersService: OffersService, private organizationService: OrganizationService) {}

  getOrganizationViewUrl(organization: Organization): string {
    return this.organizationService.getOrganizationViewUrl(organization);
  }
}

