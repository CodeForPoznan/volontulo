import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NgbAccordionModule } from '@ng-bootstrap/ng-bootstrap';

import { FaqOrganizationsComponent } from 'app/components/static/faq-organizations.component';

describe('FaqOrganizationsComponent', () => {
  let component: FaqOrganizationsComponent;
  let fixture: ComponentFixture<FaqOrganizationsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ NgbAccordionModule.forRoot() ],
      declarations: [ FaqOrganizationsComponent ],
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
