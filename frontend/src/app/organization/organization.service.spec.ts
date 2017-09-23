import { TestBed, inject } from '@angular/core/testing';
import { HttpModule } from '@angular/http';

import { OrganizationService } from './organization.service';

describe('OrganizationService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpModule],
      providers: [OrganizationService]
    });
  });

  it('should load', inject([OrganizationService], (service: OrganizationService) => {
    expect(service).toBeTruthy();
  }));
});
