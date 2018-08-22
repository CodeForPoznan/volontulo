import { TestBed, inject } from '@angular/core/testing';

import { MetatagsService } from './metatags.service';

describe('MetatagsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [MetatagsService]
    });
  });

  it('should be created', inject([MetatagsService], (service: MetatagsService) => {
    expect(service).toBeTruthy();
  }));
});
