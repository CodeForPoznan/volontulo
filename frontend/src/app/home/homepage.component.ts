import { Component, OnInit } from '@angular/core';

import { OffersService } from '../homepage-offer/offers.service';
import { Offer } from '../homepage-offer/offers.model';

@Component({
  selector: 'volontulo-home',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss'],
  providers: [OffersService]
})

export class HomePageComponent implements OnInit {
  offers: Array<Offer> = [];

  constructor(private offersService: OffersService) { }

  ngOnInit() {
    this.offersService.getOffers()
      .subscribe(
        offers => {
          this.offers = offers;
        }
      );
  }
}
