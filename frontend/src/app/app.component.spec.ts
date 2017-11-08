import { Component } from '@angular/core';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { CookieModule, CookieService } from 'ngx-cookie';
import { RouterTestingModule } from '@angular/router/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
import { CookieLawBannerComponent } from './cookie-law-banner/cookie-law-banner.component';
import { AuthService } from './auth.service';


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
