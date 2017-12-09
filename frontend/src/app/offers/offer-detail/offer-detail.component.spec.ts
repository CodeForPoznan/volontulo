import { ActivatedRoute } from '@angular/router';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { Subject } from 'rxjs/Subject';

import { IconComponent } from '../../icon/icon.component';
import { IconLabelComponent } from '../../icon-label/icon-label.component';
import { OfferDetailComponent } from './offer-detail.component';
import { OffersService } from '../../homepage-offer/offers.service';

describe('OfferDetailComponent', () => {
  let component: OfferDetailComponent;
  let fixture: ComponentFixture<OfferDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        OfferDetailComponent,
        IconLabelComponent,
        IconComponent,
      ],
      providers: [
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
