import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { combineLatest, skip, take } from 'rxjs/operators';

import { Offer } from 'app/models/offer.model';
import {
  Organization,
  OrganizationContactPayload,
  ContactStatus
} from 'app/models/organization.model';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';
import { OrganizationService } from 'app/services/organization.service';

@Component({
  selector: 'volontulo-organization',
  templateUrl: './organization.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrganizationComponent implements OnInit {
  isUserOrgMember$: Observable<boolean>;
  user$: Observable<User | null>;
  organization$: Observable<Organization>;
  contactStatus$: Observable<ContactStatus>;
  offers$: Observable<Offer[]>;

  constructor(
    private activatedRoute: ActivatedRoute,
    private organizationService: OrganizationService,
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.user$ = this.authService.user$;
    this.organization$ = this.organizationService.organization$;
    this.offers$ = this.organizationService.offers$;

    this.activatedRoute.params.subscribe(
      params => {
        this.organizationService.getOrganization(params.organizationId).subscribe();
        this.organizationService.getOffersForOrganization(params.organizationId);
      }
    );

    this.isUserOrgMember$ = this.organization$
      .pipe(
        combineLatest(this.user$, (org, user): boolean => {
          if (org === null || user === null) {
            return false;
          }
          return user.organizations.filter(organ => org.id === organ.id).length > 0;
        })
      );

    this.contactStatus$ = this.organizationService.contactStatus$;
  }

  onContact(organizationContact: OrganizationContactPayload) {
    this.organization$.pipe(take(1))
      .subscribe(org => this.organizationService.sendContactForm(org, organizationContact));
  }
}
