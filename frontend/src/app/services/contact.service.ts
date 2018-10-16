import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { environment } from 'environments/environment';


@Injectable()
export class ContactService {
  public contactAdminEndpoint = `${environment.apiRoot}/contact/`;

  constructor(private http: HttpClient) { }

  public contactAdmin(data) {
    return this.http.post<any>(this.contactAdminEndpoint, data);
  }
}
