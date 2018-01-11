import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FaqVolunteersComponent } from './faq-volunteers.component';

describe('FaqVolunteersComponent', () => {
  let component: FaqVolunteersComponent;
  let fixture: ComponentFixture<FaqVolunteersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
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
