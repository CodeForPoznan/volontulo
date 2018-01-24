import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/combineLatest';
import 'rxjs/add/operator/take';

import { Organization, OrganizationContactPayload } from './organization.model';
import { OrganizationService } from './organization.service';
import { AuthService } from '../auth.service';
import { User } from '../user';

@Component({
  selector: 'volontulo-organization',
  templateUrl: './organization.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OrganizationComponent implements OnInit {
  isUserOrgMember$: Observable<boolean>;
  user$: Observable<User | null>;
  organization$: Observable<Organization>;
  contactStatus$: Observable<string>;

  constructor(private activatedRoute: ActivatedRoute,
              private organizationService: OrganizationService,
              private authService: AuthService, ) {
  }

  ngOnInit() {
    this.user$ = this.authService.user$;

    this.organization$ = this.organizationService.organization$;

    this.activatedRoute.params
      .switchMap(params => this.organizationService.getOrganization(params.organizationId)
      ).subscribe();

    this.isUserOrgMember$ = this.organization$
      .combineLatest(this.user$, (org, user): boolean => {
        if (org === null || user === null) {
          return false;
        }
        return user.organizations.filter(organ => org.id === organ.id).length > 0;
      });
  }

  onContact(organizationContact: OrganizationContactPayload) {
    let organization: Organization;
    this.organization$.take(1).subscribe(org => organization = org);
    this.contactStatus$ = this.organizationService.sendContactForm(organization, organizationContact);
  }
}
