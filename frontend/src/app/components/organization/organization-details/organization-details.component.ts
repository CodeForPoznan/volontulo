import {Component, Input, OnInit} from '@angular/core';

import { Organization } from 'app/models/organization.model';
import { environment } from 'environments/environment';
import { MetatagsService } from 'app/services/metatags.service';


@Component({
  selector: 'volontulo-organization-details',
  templateUrl: './organization-details.component.html',
  styleUrls: ['./organization-details.component.scss'],
})

export class OrganizationDetailsComponent implements OnInit {
  @Input() isUserOrgMember: boolean;
  @Input() organization: Organization;
  djangoRoot: string = environment.djangoRoot;

  constructor(private metatagsService: MetatagsService) { }

  ngOnInit() {
    this.metatagsService.setMeta('Volontulo. Portal dla wolontariuszy', {
        'og:title': this.organization.name + ' - Volontulo. Portal dla wolontariuszy',
        'og:description': this.organization.description
      }
    );
  }
}
