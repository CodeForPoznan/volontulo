import { Injectable } from '@angular/core';
import { Http } from '@angular/http';
import { ReplaySubject } from 'rxjs/ReplaySubject';

import { environment } from '../../environments/environment';
import { Organization } from './organization.model';

@Injectable()
export class OrganizationService {
  url = `${environment.apiRoot}/organizations`;
  requestOptions = { withCredentials: true };

  querySubject: ReplaySubject<any> = new ReplaySubject(1);
  getSubject: ReplaySubject<any> = new ReplaySubject(1);

  constructor(private http: Http) {
  }

  query() {
    this.http.get(this.url, this.requestOptions)
      .subscribe(rsp => this.querySubject.next(rsp.json()));
    return this.querySubject;
  }

  get(id: number) {
    this.http.get(`${this.url}/${id}`, this.requestOptions)
      .subscribe(rsp => this.getSubject.next(rsp.json()));
    return this.getSubject;
  }

  getOrganizationViewUrl(organization: Organization): string {
    return `${environment.djangoRoot}/organizations/${organization.slug}/${organization.id}`;
  }
}
