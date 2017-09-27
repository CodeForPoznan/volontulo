import { Injectable } from '@angular/core';
import { Headers, Http, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Rx';

import { environment } from '../../environments/environment';

@Injectable()
export class OffersService {
  private url = `${environment.apiRoot}/offers/`;

  constructor (
    private http: Http
  ) {}

  getOffers() {
    return this.http.get(this.url, { withCredentials: true } )
      .map((res: Response) => res.json())
      .catch(this.handleError);
  }

  handleError(reject: Response | any) {
    const body = reject.json() || '';
    const err = body.error || JSON.stringify(body);
    return Observable.throw(err);
  }
}
