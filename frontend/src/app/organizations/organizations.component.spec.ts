import { async, ComponentFixture, TestBed, inject } from '@angular/core/testing';

import { OrganizationsComponent } from './organizations.component';
import { OrganizationService } from '../organization/organization.service';

describe('OrganizationsComponent', () => {
  let component: OrganizationsComponent;
  let fixture: ComponentFixture<OrganizationsComponent>;
  let organizationService: OrganizationService;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ OrganizationsComponent ],
      providers: [
        {
          provide: OrganizationService,
          useValue: {
            getOrganizations: jasmine.createSpy('getOrganizations'),
          },
        },
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganizationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  beforeEach(inject([OrganizationService], (_organizationsService) => {
    organizationService = _organizationsService;
  }));
});
