import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { ActivatedRoute } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { Subject } from 'rxjs/Subject';

import { OfferDetailComponent } from 'app/components/offers/offer-detail/offer-detail.component';
import { AuthService } from 'app/services/auth.service';
import { OffersService } from 'app/services/offers.service';

describe('OfferDetailComponent', () => {
  let component: OfferDetailComponent;
  let fixture: ComponentFixture<OfferDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        RouterTestingModule
      ],
      declarations: [
        OfferDetailComponent,
      ],
      schemas: [
        CUSTOM_ELEMENTS_SCHEMA
      ],
      providers: [
        {
          provide: AuthService,
          useValue: {}
        },
        {
          provide: OffersService,
          useValue: {
          },
        },
        {
          provide: ActivatedRoute,
          useValue: {
            params: new Subject()
          },
        }
      ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OfferDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
