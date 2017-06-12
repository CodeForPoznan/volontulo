import { Component } from '@angular/core';
import { TestBed, async } from '@angular/core/testing';

import { AppComponent } from './app.component';


describe('AppComponent', () => {
  beforeEach(async(() => {

    /* tslint:disable */
    @Component({selector: 'router-outlet', template: ''})
    /* tslint:enable */
    class RouterOutletStubComponent { }

    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        RouterOutletStubComponent
      ],
    }).compileComponents();
  }));

  it('should create the app', async(() => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  }));

});
