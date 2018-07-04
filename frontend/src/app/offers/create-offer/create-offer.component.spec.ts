import { ActivatedRoute } from '@angular/router';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { Subject } from 'rxjs/Subject';

import { AuthService } from '../../auth.service';
import { CreateOfferComponent } from './create-offer.component';
import { OffersService } from '../../homepage-offer/offers.service';

describe('CreateOfferComponent', () => {
  let component: CreateOfferComponent;
  let fixture: ComponentFixture<CreateOfferComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule,
        ReactiveFormsModule,
        RouterTestingModule,
      ],
      declarations: [ CreateOfferComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: {
            params: new Subject()
          },
        },
      {
        provide: AuthService,
        useValue: {
          user$: new Subject(),
        }
      },
      {
        provide: OffersService,
        useValue: {},
      }
    ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateOfferComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  })

  describe('startedAt and finishedAt validation', () => {
    it('should set invalid status when startedAt and actionOngoing are filled', () => {
      component.form.patchValue({
        startedAt: '2010/05/10',
        actionOngoing: true,
      });

      expect(component.form.errors.hasOwnProperty('startedAtError')).toBe(true);
      expect(component.form.errors.startedAtError).toBe(true);
    });

    it('should set invalid status when finishedAt and constantCoop are filled', () => {
      component.form.patchValue({
        finishedAt: '2010/05/10',
        constantCoop: true,
      });

      expect(component.form.valid).toBe(false);
    });

    it('shouldn\'t set invalid status when startedAt and constantCoop are filled', () => {
      component.form.patchValue({
        startedAt: '2010/05/10',
        constantCoop: true,
      });

      expect(component.form.errors).toBeNull();
    });

    it('shouldn\'t set invalid status when finishedAt and actionOngoing are filled', () => {
      component.form.patchValue({
        finishedAt: '2010/05/10',
        actionOngoing: true,
      });

      expect(component.form.errors).toBeNull();
    });

    it('should display error message if startedAt and actionOngoing are invalid', () => {
      component.form.patchValue({
        startedAt: '2010/03/02',
        finishedAt: '2010/05/10',
        actionOngoing: true,
        constantCoop: true,
      });
      component.hasOrganization = true;
      fixture.detectChanges();

      const errorFinishedAtElem = fixture.debugElement.query(By.css('.finishedAt .errors span'));
      const errorStartedAtElem = fixture.debugElement.query(By.css('.startedAt .errors span'));
      expect(errorFinishedAtElem).not.toBeNull();
      expect(errorFinishedAtElem.nativeElement.innerText).toContain('nie podawaj daty');
      expect(errorStartedAtElem).not.toBeNull();
      expect(errorStartedAtElem.nativeElement.innerText).toContain('nie podawaj daty');
    });
  });
});
