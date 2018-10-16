import { Component, OnDestroy, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable } from 'rxjs/Observable';
import { filter, map, switchMap, take, tap } from 'rxjs/operators';
import { Subscription } from 'rxjs/Subscription';

import { Organization } from 'app/models/organization.model';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';
import { OrganizationService } from 'app/services/organization.service';
import { UserService } from 'app/services/user.service';

@Component({
  selector: 'volontulo-organization-create',
  templateUrl: './organization-create.component.html',
  styleUrls: ['./organization-create.component.scss']
})
export class OrganizationCreateComponent implements OnInit, OnDestroy {
  createForm: FormGroup;
  id: number;
  message = '';
  createSubscription: Subscription;
  organization$: Observable<Organization>;
  user: User;

  constructor(
    private authService: AuthService,
    private activatedRoute: ActivatedRoute,
    private fb: FormBuilder,
    private organizationService: OrganizationService,
    private router: Router,
    private userService: UserService,
    ) {}

  ngOnInit() {
    this.authService.user$.pipe(take(1))
      .subscribe(
      (user: User) => { this.user = user }
    );

    this.createForm = this.fb.group({
       'name': this.fb.control(null, Validators.required),
       'address': this.fb.control(null, Validators.required),
       'description': this.fb.control(null, Validators.required),
      });

    this.organization$ = this.activatedRoute.params.pipe(
      map(params => params.organizationId),
      filter(organizationId => !!organizationId),
      switchMap(organizationId => this.organizationService.getOrganization(organizationId)),
      tap(organization => this.createForm.patchValue(organization))
    );

    this.createSubscription = this.organizationService.createOrEditOrganization$
      .subscribe(
        (response) => {
          if (response.type !== 'error') {
            if (response.type === 'edit') {
              this.userService.updateOrganization(response.data).subscribe();
            } else {
              this.userService.addOrganization(response.data).subscribe();
            }
            this.router.navigate(['/organizations', response.data.slug, response.data.id]);
          } else {
            this.message = response.data.detail;
          }
      });
  }

  onSubmit() {
    const id = this.activatedRoute.snapshot.params.organizationId;
    if (id) {
      this.organizationService.editOrganization(id, this.createForm.value);
    } else {
      this.organizationService.createOrganization(this.createForm.value);
    }
  }

  isFormInputInvalid(inputStringId: string): boolean {
    return this.createForm.get(inputStringId).invalid && this.createForm.get(inputStringId).touched;
  }

  ngOnDestroy() {
    this.createSubscription.unsubscribe();
  }
}
