import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';


import { Offer } from 'app/models/offer.model';
import {
  Organization,
  OrganizationContactPayload,
  ContactStatus,
  CreateOrEditOrganization
} from 'app/models/organization.model';
import { loadDefaultImage } from 'app/utils/offer.utils';
import { environment } from 'environments/environment';

@Injectable()
export class OrganizationService {
  private url = `${environment.apiRoot}/organizations/`;

  private contactStatusEvent = new Subject<ContactStatus>();
  private organizationEvent = new BehaviorSubject<Organization | null>(null);
  private organizationsEvent = new Subject<Organization[]>();
  private offersEvent = new Subject<Offer[]>();
  private createOrganizationEvent = new Subject<CreateOrEditOrganization>();

  public contactStatus$: Observable<ContactStatus> = this.contactStatusEvent.asObservable();
  public organization$: Observable<Organization | null> = this.organizationEvent.asObservable();
  public organizations$: Observable<Organization[]> = this.organizationsEvent.asObservable();
  public offers$: Observable<Offer[]> = this.offersEvent.asObservable();
  public createOrEditOrganization$: Observable<CreateOrEditOrganization> = this.createOrganizationEvent.asObservable();

  constructor(private http: HttpClient) { }

  getOrganization(id: number): Observable<Organization> {
    return this.http.get<Organization>(`${this.url}${id}/`)
      .map(organization => {
        this.organizationEvent.next(organization);
        return organization;
      });
  }

  sendContactForm(organization: Organization, contactData: OrganizationContactPayload) {
    this.http.post(
      `${this.url}${organization.id}/contact/`,
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

  createOrganization(newOrganization: Organization) {
    this.http.post(this.url, newOrganization)
      .subscribe(
        (data: HttpResponse<Organization>) => {
          this.createOrganizationEvent.next({data, type: 'create'});
        },
        error => {this.createOrganizationEvent.next({ data: error.error, type: 'error'})
        });
  }
  editOrganization(id: number, updatedOrganization: Organization) {
    this.http.put(`${this.url}${id}/`, updatedOrganization)
      .subscribe( (data: HttpResponse<Organization>) => {
          this.createOrganizationEvent.next({data, type: 'edit'});
        },
        error => {
        this.createOrganizationEvent.next({ data: error.error, type: 'error'});
      });
  }

  getOrganizations() {
    return this.http.get<Organization[]>(this.url)
      .subscribe(organizations => this.organizationsEvent.next(organizations));
  }

  getOffersForOrganization(id: number) {
    return this.http.get<Offer[]>(`${this.url}${id}/offers/`)
      .map(offers => offers.map(offer => loadDefaultImage(offer)))
      .subscribe(offers => this.offersEvent.next(offers));
  }
}
