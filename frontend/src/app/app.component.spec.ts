import { Component } from '@angular/core';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { AppComponent } from './app.component';
import { HeaderComponent } from './header/header.component';
import { FooterComponent } from './footer/footer.component';
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
        HttpModule
      ],
      declarations: [
        AppComponent,
        RouterOutletStubComponent,
        HeaderComponent,
        FooterComponent
      ],
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
