import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import 'rxjs/add/operator/map';
import { Observable } from 'rxjs/Observable';

import { environment } from '../../environments/environment';
import { loadDefaultImage } from './offer.utils';
import { Offer } from './offers.model';


@Injectable()
export class OffersService {
  private url = `${environment.apiRoot}/offers/`;

  constructor (private http: HttpClient) { }

  getOffers(): Observable<Offer[]> {
    return this.http.get<Offer[]>(this.url)
      .map(offers => offers.map(offer => loadDefaultImage(offer)));
  }

  getOffer(id: number): Observable<Offer> {
    return this.http.get<Offer>(`${this.url}${id}/`)
      .map(offer => loadDefaultImage(offer));
  }

  getJoinViewUrl(offer: Offer): string {
    return `${environment.djangoRoot}/offers/${offer.slug}/${offer.id}/join`;
  }

}
