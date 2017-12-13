import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/combineLatest';
import 'rxjs/add/operator/switchMap';

import { Organization } from './organization.model';
import { OrganizationService } from './organization.service';
import { AuthService } from '../auth.service';
import { User } from '../user';
import { environment } from '../../environments/environment';

@Component({
  selector: 'volontulo-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.css'],
})

export class OrganizationDetailsComponent implements OnInit {
  djangoRoot: string = environment.djangoRoot;
  isUserOrgMember$: Observable<boolean>;
  organization$: Observable<Organization>;
  user$: Observable<User | null>;

  constructor(
    private activatedRoute: ActivatedRoute,
    private organizationService: OrganizationService,
    private authService: AuthService,
  ) {}

  ngOnInit() {
    this.user$ = this.authService.user$;

    this.organization$ = this.activatedRoute.params
      .switchMap(params => this.organizationService.getOrganization(params.organizationId));

    this.isUserOrgMember$ = this.organization$
      .combineLatest(this.user$, (org, user) => {
        return user.organizations.filter(organ => org.id === organ.id).length > 0;
      });
  }
}
