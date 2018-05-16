import { Component, OnInit } from '@angular/core';

import { OffersService } from '../homepage-offer/offers.service';
import { ApiOffer } from '../homepage-offer/offers.model';

@Component({
  selector: 'volontulo-home',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss'],
  providers: [OffersService]
})

export class HomePageComponent implements OnInit {
  offers: Array<ApiOffer> = [];

  constructor(private offersService: OffersService) { }

  ngOnInit() {
    this.offersService.getOffers()
      .subscribe(offers => this.offers = offers);
  }
}
