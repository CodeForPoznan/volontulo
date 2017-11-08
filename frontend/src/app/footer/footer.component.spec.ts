import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { CommonModule } from '@angular/common';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { FooterComponent } from './footer.component';
import { AuthService } from '../auth.service';
import { AboutUsComponent } from '../static/about-us.component';
import { RegulationsComponent } from '../static/regulations.component';


describe('FooterComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        HttpModule,
        CommonModule,
        RouterTestingModule.withRoutes([
          { path: 'o-nas', component: AboutUsComponent },
          { path: 'regulations', component: RegulationsComponent }
        ])
      ],
      declarations: [
        FooterComponent, AboutUsComponent, RegulationsComponent
      ],
    }).compileComponents();
  });

  it('should create the footer', async(() => {
    inject([AuthService], () => {
      const fixture = TestBed.createComponent(FooterComponent);
      const footer = fixture.debugElement.componentInstance;
      expect(footer).toBeTruthy();
    });
  }));
});
