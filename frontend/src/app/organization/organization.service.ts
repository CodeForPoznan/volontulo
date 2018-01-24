import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';

import { Organization, OrganizationContactPayload } from './organization.model';
import { environment } from '../../environments/environment';

@Injectable()
export class OrganizationService {
  url = `${environment.apiRoot}/organizations`;
  requestOptions = { withCredentials: true };
  private _organization$ = new BehaviorSubject<Organization>(null);
  public organization$ = this._organization$.asObservable();

  constructor(private http: Http) {
  }

  getOrganization(id: number): Observable<Organization> {
    return this.http.get(`${this.url}/${id}/`, this.requestOptions).map(response => {
      this._organization$.next(response.json());
      return response.json();
    });
  }

  sendContactForm(organization: Organization, contactData: OrganizationContactPayload): Observable<string> {
    return this.http.post(
      `${environment.apiRoot}/organizations/${organization.id}/contact/`,
      contactData)
      .map(response => {
        if (response.status === 201) {
          return 'success';
        }
      }).catch(err => Observable.of('error'));
  }

  getOrganizationViewUrl(organization: Organization): string {
    return `${environment.djangoRoot}/organizations/${organization.slug}/${organization.id}`;
  }
}
