import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SubFooterComponent } from './sub-footer.component';

describe('SubFooterComponent', () => {
  let component: SubFooterComponent;
  let fixture: ComponentFixture<SubFooterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SubFooterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SubFooterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
