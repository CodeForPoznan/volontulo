import { Component, OnInit } from '@angular/core';
import { Organization } from '../organization/organization.model';
import { OrganizationService } from '../organization/organization.service';
import { Observable } from 'rxjs/Observable';

@Component({
  selector: 'volontulo-organizations',
  templateUrl: './organizations.component.html'
})
export class OrganizationsComponent implements OnInit {
  public organizations$: Observable<Organization[]>;

  constructor(
    private organizationService: OrganizationService
  ) { }

  ngOnInit() {
    this.organizations$ = this.organizationService.organizations$;
    this.organizationService.getOrganizations();
  }

  getOrganizationViewUrl(organization: Organization): string {
    return this.organizationService.getOrganizationViewUrl(organization);
  }

  getOrganizationCreateViewUrl(): string {
    return this.organizationService.getOrganizationCreateViewUrl();
  }
}
