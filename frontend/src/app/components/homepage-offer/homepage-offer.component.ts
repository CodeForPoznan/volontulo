import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

import { Offer } from 'app/models/offer.model';
import { OffersService } from 'app/services/offers.service';
import { OrganizationService } from 'app/services/organization.service';

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

