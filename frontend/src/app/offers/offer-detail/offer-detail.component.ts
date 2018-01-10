import 'rxjs/add/operator/switchMap';
import { ActivatedRoute } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { environment } from '../../../environments/environment';
import { Offer } from '../../homepage-offer/offers.model';
import { OffersService } from '../../homepage-offer/offers.service';

@Component({
  selector: 'volontulo-offer-detail',
  templateUrl: './offer-detail.component.html',
  styleUrls: ['./offer-detail.component.css'],
})
export class OfferDetailComponent implements OnInit {
  public offer$: Observable<Offer>;
  public djangoRoot = environment.djangoRoot;
  public getJoinViewUrl = this.offersService.getJoinViewUrl;

  constructor(
    private activatedRoute: ActivatedRoute,
    private offersService: OffersService,
  ) { }

  ngOnInit() {
    this.offer$ = this.activatedRoute.params
    .switchMap(params => this.offersService.getOffer(params.offerId));
  }
}
