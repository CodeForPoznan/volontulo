import { Component, OnInit } from '@angular/core';

import { Offer } from 'app/models/offer.model';
import { OffersService } from 'app/services/offers.service';

@Component({
  selector: 'volontulo-home',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss'],
  providers: [OffersService]
})

export class HomePageComponent implements OnInit {
  offers: Offer[] = [];

  constructor(private offersService: OffersService) { }

  ngOnInit() {
    this.offersService.getOffers()
      .subscribe(offers => this.offers = offers);
  }
}
