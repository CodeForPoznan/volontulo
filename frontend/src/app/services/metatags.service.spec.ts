import { TestBed, inject } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { MetatagsService } from 'app/services/metatags.service';

describe('MetatagsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      providers: [MetatagsService]
    });
  });

  it('should be created', inject([MetatagsService], (service: MetatagsService) => {
    expect(service).toBeTruthy();
  }));
});
