import { Location } from '@angular/common';
import { DebugElement } from '@angular/core';
import { async, ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';

import { OrganizationsListComponent } from './organizations-list.component';

describe('OrganizationsComponent', () => {

  let component: OrganizationsListComponent;
  let fixture: ComponentFixture<OrganizationsListComponent>;
  let debugElement: DebugElement;
  let location: Location;
  const organizations = [{
      address: 'Winterfell, ul. Przed Murem 1',
      description: 'Winter is comming',
      id: 93,
      name: 'Starks Family',
      slug: 'stark-family',
      url: 'http://localhost:4200/api/organizations/93/'
    }, {
      address: 'Casterly Rock',
      description: 'A Lannister always pays his debts.',
      id: 94,
      name: 'Lannister Family',
      slug: 'lannister-family',
      url: 'http://localhost:4200/api/organizations/94/',
    }, ];

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [OrganizationsListComponent],
      imports: [RouterTestingModule.withRoutes([
        {
          path: 'organizations/create',
          component: OrganizationsListComponent,
        },
        {
          path: 'organizations/:organizationSlug/:organizationId',
          component: OrganizationsListComponent,
        }
      ])],
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(OrganizationsListComponent);
    component = fixture.componentInstance;
    debugElement = fixture.debugElement;
    fixture.detectChanges();
    location = TestBed.get(Location);
  });

  it('should create component', () => {
    expect(component).toBeTruthy();
  });

  it('should render \'p\' element with information that there are no organizations', () => {
    component.organizations = [];
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('p').length).toBe(1);
    expect(fixture.nativeElement.querySelector('p').innerText).toEqual('Brak zdefiniowanych organizacji.');
  });

  it('should render two organizations on the list', () => {
    component.organizations = organizations;
    fixture.detectChanges();
    expect(fixture.nativeElement.querySelectorAll('td').length).toBe(4);
  });

  it('should navigate to /organizations/create when button was clicked', fakeAsync(() => {
    debugElement.nativeElement.querySelector('.btn').click();
    tick();
    expect(location.path()).toEqual('/organizations/create');
  }));

  it('should navigate to /organizations/slug/id when clicked on name', fakeAsync(() => {
   component.organizations = organizations;
   fixture.detectChanges();
   debugElement.nativeElement.querySelectorAll('.organization-detail')[0].click();
   tick();
   expect(location.path()).toEqual(`/organizations/${organizations[0].slug}/${organizations[0].id}`);
  }));
});
