import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';

import { Organization } from 'app/models/organization.model';
import { OrganizationService } from 'app/services/organization.service';

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
}
