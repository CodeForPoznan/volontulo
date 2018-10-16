import { CommonModule } from '@angular/common';
import { TestBed, inject, async } from '@angular/core/testing';
import { HttpModule } from '@angular/http';
import { RouterTestingModule } from '@angular/router/testing';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

import { FooterComponent } from 'app/components/footer/footer.component';
import { AboutUsComponent } from 'app/components/static/about-us.component';
import { RegulationsComponent } from 'app/components/static/regulations.component';
import { AuthService } from 'app/services/auth.service';


describe('FooterComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [
        NgbModule.forRoot(),
        HttpModule,
        CommonModule,
        RouterTestingModule.withRoutes([
          { path: 'about-us', component: AboutUsComponent },
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
