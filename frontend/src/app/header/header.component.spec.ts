import { Component } from '@angular/core';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { HeaderComponent } from './header.component';
import { AuthService } from '../auth.service';
import { RouterTestingModule } from '@angular/router/testing';

describe('HeaderComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        HttpModule,
        RouterTestingModule,
      ],
      providers: [
      ],
      declarations: [
        HeaderComponent
      ],
    }).compileComponents();
  });

  it('should create the header', async(() => {
    inject([AuthService], () => {
      const fixture = TestBed.createComponent(HeaderComponent);
      const header = fixture.debugElement.componentInstance;
      expect(header).toBeTruthy();
    });
  }));
});
