import { Component } from '@angular/core';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { FooterComponent } from './footer.component';
import { AuthService } from '../auth.service';


describe('FooterComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        HttpModule
      ],
      providers: [
      ],
      declarations: [
        FooterComponent
      ],
    }).compileComponents();
  });

  it('should create the footer', async(() => {
    inject([AuthService], () => {
      const fixture = TestBed.createComponent(FooterComponent);
      const foter = fixture.debugElement.componentInstance;
      expect(footer).toBeTruthy();
    });
  }));
});
