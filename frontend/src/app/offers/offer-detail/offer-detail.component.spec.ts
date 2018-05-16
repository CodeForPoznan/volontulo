import { ActivatedRoute } from '@angular/router';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Subject } from 'rxjs/Subject';

import { AuthService } from '../../auth.service';
import { IconComponent } from '../../icon/icon.component';
import { IconLabelComponent } from '../../icon-label/icon-label.component';
import { OfferDetailComponent } from './offer-detail.component';
import { OffersService } from '../../homepage-offer/offers.service';

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
        IconLabelComponent,
        IconComponent,
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
