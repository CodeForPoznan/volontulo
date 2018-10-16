import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs/Observable';

import { environment } from 'environments/environment';


export interface ContactData {
  administratorEmails: string[];
  applicantTypes: string[];
}


@Injectable()
export class ContactResolver implements Resolve<ContactData> {
  constructor(private http: HttpClient) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ContactData> {
    return this.http.get<ContactData>(`${environment.apiRoot}/contact/`);
  }
}
