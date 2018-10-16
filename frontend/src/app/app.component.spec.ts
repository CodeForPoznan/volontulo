import { Component, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CookieModule, CookieService } from 'ngx-cookie';

import { AppComponent } from 'app/app.component';
import { FooterComponent } from 'app/components/footer/footer.component';
import { HeaderComponent } from 'app/components/header/header.component';
import { CookieLawBannerComponent } from 'app/components/cookie-law-banner/cookie-law-banner.component';
import { AuthService } from 'app/services/auth.service';


describe('AppComponent', () => {
  beforeEach(async(() => {

    /* tslint:disable */
    @Component({ selector: 'router-outlet', template: '' })
      /* tslint:enable */
    class RouterOutletStubComponent {
    }

    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        CookieModule.forRoot(),
        HttpModule,
        RouterTestingModule
      ],
      providers: [
        CookieService
      ],
      declarations: [
        AppComponent,
        RouterOutletStubComponent,
        HeaderComponent,
        FooterComponent,
        CookieLawBannerComponent
      ],
      schemas: [
        CUSTOM_ELEMENTS_SCHEMA
      ]
    }).compileComponents();
  }));

  it('should create the app', async(() => {
    inject([AuthService], () => {
      const fixture = TestBed.createComponent(AppComponent);
      const app = fixture.debugElement.componentInstance;
      expect(app).toBeTruthy();
    });
  }));

});
