import { NO_ERRORS_SCHEMA, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { FormBuilder, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { UserProfileComponent } from './user-profile.component';
import { AuthService } from '../auth.service';
import { User } from '../user';


describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UserProfileComponent ],
      schemas: [
        NO_ERRORS_SCHEMA,
        CUSTOM_ELEMENTS_SCHEMA
      ],
      providers: [ AuthService, FormBuilder ],
      imports: [ HttpClientTestingModule, RouterTestingModule, ReactiveFormsModule, FormsModule],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('form should be invalid when empty', () => {
    expect(component.fg.valid).toBeFalsy();
  });

  it('phone no field validation', () => {
    let errors = {};
    const phone_no = component.fg.controls['phone_no'];

    // phone no field shoud be required
    errors = phone_no.errors || {};
    expect(errors['required']).toBeTruthy();

    // phone no should be invalid according to pattern
    phone_no.setValue('a11222333');
    errors = phone_no.errors || {};
    expect(errors['pattern']).toBeTruthy();

    // phone no should be invalid according to maxlength validation
    phone_no.setValue('0111222333');
    errors = phone_no.errors || {};
    expect(errors['maxlength']).toBeTruthy();

    // set phone no to correct value
    phone_no.setValue('111222333');
    errors = phone_no.errors || {};
    expect(errors['required']).toBeFalsy();
    expect(errors['maxlength']).toBeFalsy();
    expect(errors['pattern']).toBeFalsy();
  });
});
