import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { NgbAccordionModule } from '@ng-bootstrap/ng-bootstrap';

import { FaqVolunteersComponent } from 'app/components/static/faq-volunteers.component';

describe('FaqVolunteersComponent', () => {
  let component: FaqVolunteersComponent;
  let fixture: ComponentFixture<FaqVolunteersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ NgbAccordionModule.forRoot() ],
      declarations: [ FaqVolunteersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FaqVolunteersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
