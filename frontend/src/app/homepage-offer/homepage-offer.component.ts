import { Component, OnInit, Input } from '@angular/core';

import { Offer } from './offers.model';
import { OffersService } from './offers.service';

@Component({
  selector: 'volontulo-homepage-offer',
  templateUrl: './homepage-offer.component.html',
  styleUrls: ['./homepage-offer.component.css'],
  providers: [OffersService]
})
export class HomepageOfferComponent {
  @Input() offer: Offer;

  constructor(private offersService: OffersService) {}

  getDjangoViewUrl(offer: Offer): string {
    return this.offersService.getDjangoViewUrl(offer);
  }
}

