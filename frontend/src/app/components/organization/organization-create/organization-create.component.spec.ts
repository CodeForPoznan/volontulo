import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, TestBed, ComponentFixture } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';

import { OrganizationCreateComponent } from 'app/components/organization/organization-create/organization-create.component';
import { AuthService } from 'app/services/auth.service';
import { OrganizationService } from 'app/services/organization.service';
import { UserService } from 'app/services/user.service';

describe('OrganizationCreateComponent', () => {
  let component: OrganizationCreateComponent;
  let fixture: ComponentFixture<OrganizationCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
       imports: [
        ReactiveFormsModule,
        HttpClientTestingModule,
        RouterTestingModule,
      ],
      declarations: [ OrganizationCreateComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [ OrganizationService, AuthService, UserService ],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganizationCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
