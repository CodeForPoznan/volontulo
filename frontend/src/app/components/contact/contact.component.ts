import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { filter, finalize, take } from 'rxjs/operators';

import { ContactData } from 'app/resolvers';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';
import { ContactService } from 'app/services/contact.service';
import { UserService } from 'app/services/user.service';

@Component({
  selector: 'volontulo-contact',
  templateUrl: './contact.component.html',
})
export class ContactComponent implements OnInit {
  public contactData: ContactData;
  public fg: FormGroup = this.fb.group({
    applicant_type: ['', [Validators.required]],
    applicant_email: ['', [Validators.required, Validators.email]],
    applicant_name: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(150)]],
    administrator_email: ['', [Validators.required, Validators.email]],
    message: ['', [Validators.required, Validators.minLength(10), Validators.maxLength(2000)]],
    phone_no: ['', [Validators.required, Validators.minLength(9), Validators.maxLength(9), Validators.pattern(/^[0-9]{9}$/)]],
    honey_value: ['']
  });

  public submitEnabled = true;
  public success: null | boolean = null;

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private contactService: ContactService,
    private authService: AuthService,
    private userService: UserService,
  ) { }

  ngOnInit() {
    this.route.data.subscribe(
      data => {
        this.contactData = data.contactData;
        this.fg.controls.applicant_type.setValue(this.contactData.applicantTypes[0]);
        this.fg.controls.administrator_email.setValue(this.contactData.administratorEmails[0]);
      }
    );
    this.authService.user$
      .pipe(
        filter(user => user !== null),
        take(1),
      )
      .subscribe(
        (user: User) => {
          this.fg.controls.applicant_email.setValue(user.email);
          this.fg.controls.applicant_name.setValue(this.userService.getFullName(user));
          this.fg.controls.phone_no.setValue(user.phoneNo);
        }
      )
  }

  submitForm() {
    if (this.fg.valid && !this.fg.value.honey_value) {
      this.submitEnabled = false;
      delete this.fg.value.honey_value;

      this.contactService.contactAdmin(this.fg.value)
        .pipe(finalize(() => this.submitEnabled = true))
        .subscribe(
          () => {
            this.success = true;
            this.fg.reset({
              applicant_type: this.contactData.applicantTypes[0],
              administrator_email: this.contactData.administratorEmails[0],
            });
          },
          () => this.success = false,
        );
    }
  }

}
