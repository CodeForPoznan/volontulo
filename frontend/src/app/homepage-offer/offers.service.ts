import { Offer } from './offers.model';
import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { environment } from '../../environments/environment';



@Injectable()
export class OffersService {
  private url = `${environment.apiRoot}/offers/`;
  constructor (private http: Http) { }

  getOffers() {
    return this.http.get(this.url, { withCredentials: true } )
      .map((res: Response) => res.json())
      .map(offers => {
        for (const offer of offers) {
          this.loadDefaultImage(offer);
        }
        return offers;
      });
  }

  getOffer(id: number): Observable<Offer> {
    return this.http.get(`${this.url}${id}/`, { withCredentials: true })
      .map((res: Response) => res.json())
      .map(offer => this.loadDefaultImage(offer));
  }

  loadDefaultImage(offer: Offer): Offer {
    if (offer.image === null) {
        offer.image = 'assets/img/banner/volontulo_baner.png';
    }
    return offer;
  }

  getJoinViewUrl(offer: Offer): string {
    return `${environment.djangoRoot}/offers/${offer.slug}/${offer.id}/join`;
  }

}
