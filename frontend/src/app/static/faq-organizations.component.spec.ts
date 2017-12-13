import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FaqOrganizationsComponent } from './faq-organizations.component';

describe('FaqOrganizationsComponent', () => {
  let component: FaqOrganizationsComponent;
  let fixture: ComponentFixture<FaqOrganizationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FaqOrganizationsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FaqOrganizationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
