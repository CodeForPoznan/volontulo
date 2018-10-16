import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';
import { Observable } from 'rxjs/Observable';

import { ContactStatus, OrganizationContactPayload } from 'app/models/organization.model';
import { User } from 'app/models/user.model';
import { AuthService } from 'app/services/auth.service';
import { UserService } from 'app/services/user.service';

@Component({
  selector: 'volontulo-organization-contact',
  templateUrl: './organization-contact.component.html',
  styleUrls: ['./organization-contact.component.scss']
})
export class OrganizationContactComponent implements OnChanges {
  @ViewChild('contactForm') contactForm: NgForm;
  @Output() contact = new EventEmitter<OrganizationContactPayload>();
  @Input() contactStatus: ContactStatus;
  submitDisabled = false;
  alertSuccessClosed = true;
  alertErrorClosed = true;
  user$: Observable<User> = this.authService.user$;
  getFullName = this.userService.getFullName;

  constructor(private authService: AuthService, private userService: UserService) {
  }

  ngOnChanges(changes: SimpleChanges) {
    if (changes.contactStatus.currentValue && changes.contactStatus.currentValue.status === 'success') {
      this.alertSuccessClosed = false;
      this.contactForm.reset();
    } else if (changes.contactStatus.currentValue && changes.contactStatus.currentValue.status === 'error') {
      this.alertErrorClosed = false;
    }
    this.submitDisabled = false;
  }

  onSubmit() {
    if (!this.contactForm.value.honeyBunny) {
      this.contact.emit(this.contactForm.value as OrganizationContactPayload);
      this.submitDisabled = true;
    }
  }
}
