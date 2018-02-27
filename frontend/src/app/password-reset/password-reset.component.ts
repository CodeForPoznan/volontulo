import { Component, ViewChild } from '@angular/core';
import { NgForm } from '@angular/forms';

import { AuthService } from '../auth.service';

@Component({
  selector: 'volontulo-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
})
export class PasswordResetComponent {
  @ViewChild('resetForm') resetForm: NgForm;
  alertSuccessVisible = false;

  constructor(private authService: AuthService) { }

  onSubmit(): void {
    this.authService.resetPassword(this.resetForm.value.username)
      .subscribe(status => {
        if (status === 'success') {
          this.alertSuccessVisible = true;
          this.resetForm.reset();
        }
      });
  }
  hideSuccessAlert() {
    this.alertSuccessVisible = false;
  }
}
