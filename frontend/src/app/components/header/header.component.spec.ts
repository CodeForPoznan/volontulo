import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { HeaderComponent } from 'app/components/header/header.component';
import { AuthService } from 'app/services/auth.service';

describe('HeaderComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        HttpModule,
        RouterTestingModule,
      ],
      providers: [
      ],
      declarations: [
        HeaderComponent
      ],
    }).compileComponents();
  });

  it('should create the header', async(() => {
    inject([AuthService], () => {
      const fixture = TestBed.createComponent(HeaderComponent);
      const header = fixture.debugElement.componentInstance;
      expect(header).toBeTruthy();
    });
  }));
});
