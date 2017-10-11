import { Injectable } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';

import { environment } from '../../environments/environment';

@Injectable()
export class OffersService {
  private url = `${environment.apiRoot}/offers/`;

  constructor (private http: Http) { }

  getOffers() {
    return this.http.get(this.url, { withCredentials: true } )
      .map((res: Response) => res.json());
  }
}
