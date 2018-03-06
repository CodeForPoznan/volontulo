import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';

import { Organization, OrganizationContactPayload } from './organization.model';
import { ContactStatus } from './organization.interfaces';
import { environment } from '../../environments/environment';

@Injectable()
export class OrganizationService {
  url = `${environment.apiRoot}/organizations`;
  private contactStatusEvent = new BehaviorSubject<ContactStatus | null>(null);
  private organizationEvent = new BehaviorSubject<Organization | null>(null);
  private organizationsEvent = new BehaviorSubject<Organization[] | null>(null);

  public contactStatus$: Observable<ContactStatus | null> = this.contactStatusEvent.asObservable();
  public organization$: Observable<Organization | null> = this.organizationEvent.asObservable();
  public organizations$: Observable<Organization[] | null> = this.organizationsEvent.asObservable();

  constructor(private http: HttpClient) { }

  getOrganization(id: number) {
    return this.http.get<Organization>(`${this.url}/${id}/`)
      .subscribe(organization => this.organizationEvent.next(organization));
  }

  sendContactForm(organization: Organization, contactData: OrganizationContactPayload) {
    this.http.post(
      `${environment.apiRoot}/organizations/${organization.id}/contact/`,
      contactData,
      { observe: 'response' })
      .subscribe(
        (response: HttpResponse<any>) => {
          if (response.status !== 201) {
            this.contactStatusEvent.next({ data: contactData, status: 'error' });
          } else {
            this.contactStatusEvent.next({ data: contactData, status: 'success' });
          }
        },
        err => this.contactStatusEvent.next({ data: contactData, status: 'error' }),
      );
  }

  getOrganizationViewUrl(organization: Organization): string {
    return `${environment.djangoRoot}/organizations/${organization.slug}/${organization.id}`;
  }

  getOrganizationCreateViewUrl(): string {
    return `${environment.djangoRoot}/organizations/create`;
  }

  getOrganizations() {
    return this.http.get<Organization[]>(this.url)
      .subscribe(organizations => this.organizationsEvent.next(organizations));
  }
}
