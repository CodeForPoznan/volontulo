import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

import { Offer } from './offers.model';
import { OffersService } from './offers.service';
import { OrganizationService } from '../organization/organization.service';

@Component({
  selector: 'volontulo-homepage-offer',
  templateUrl: './homepage-offer.component.html',
  styleUrls: ['./homepage-offer.component.scss'],
  providers: [OffersService, OrganizationService],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class HomepageOfferComponent {
  @Input() offer: Offer;
}

